# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = "stock.move"

    #TODO: this field may not be needed
    qty_to_reserve = fields.Float(
        "Quantity to Reserve",
        compute="_compute_qty_to_reserve",
        digits=dp.get_precision("Product Unit of Measure"),
        readonly=True,
        help="Quantity that is expected to be reserved for this move.",
    )
    quant_ids = fields.Many2many("stock.quant", string="Quants")
    has_quant = fields.Boolean(compute="_compute_has_quant")
    should_reserve_stock = fields.Boolean(compute="_compute_should_reserve_stock")

    @api.depends("quant_ids")
    def _compute_has_quant(self):
        for move in self:
            if move.quant_ids:
                move.has_quant = True

    @api.depends("active_move_line_ids.quant_available_uom_qty", "active_move_line_ids.uom_qty_to_reserve", "active_move_line_ids.product_uom_qty")
    def _compute_should_reserve_stock(self):
        for move in self:
            for line in move.active_move_line_ids:
                if line.uom_qty_to_reserve != line.product_uom_qty and line.uom_qty_to_reserve <= line.quant_available_uom_qty:
                    move.should_reserve_stock = True
                    break

    @api.multi
    @api.depends("move_line_ids.qty_to_reserve")
    def _compute_qty_to_reserve(self):
        result = {
            data["move_id"][0]: data["qty_to_reserve"]
            for data in self.env["stock.move.line"].read_group(
                [("move_id", "in", self.ids)],
                ["move_id", "qty_to_reserve"],
                ["move_id"],
            )
        }
        for rec in self:
            qty_to_reserve = rec.product_id.uom_id._compute_quantity(
                result.get(rec.id, 0.0), rec.product_uom, rounding_method="HALF-UP"
            )
            if rec.product_qty >= rec.reserved_availability + qty_to_reserve:
                rec.qty_to_reserve = qty_to_reserve
            else:
                raise UserError(_("You are trying to reserve more than needed."))

    # def _update_reserved_quantity_component(self, location_id, strict=True):
    def _update_reserved_quantity_component(self, location_id):
        """Unlike the standard method _update_reserved_quantity(), we will not
        create move lines here. We will just try updating reserved quantities
        of quants to keep consistency between existing move lines and quants.
        """
        self.ensure_one()
        taken_quantity = 0
        rounding = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for line in self.move_line_ids:
            available_quantity = self.env["stock.quant"]._get_available_quantity(
                line.product_id, line.location_id, line.lot_id
            )
            if available_quantity <= 0:
                continue
            # missing_qty could go negative here, and that is OK.
            missing_qty = line.qty_to_reserve - line.product_qty
            quantity = min(missing_qty, available_quantity)
            # See comments in the standard method _update_reserved_quantity()
            # for the rationale of following conversions.
            quantity_move_uom = self.product_id.uom_id._compute_quantity(
                quantity, self.product_uom, rounding_method="DOWN"
            )
            quantity = self.product_uom._compute_quantity(
                quantity_move_uom, self.product_id.uom_id, rounding_method="HALF-UP"
            )
            quants = []
            # TODO: should we remove the case of serial?
            # if self.product_id.tracking == 'serial':
            #     if float_compare(quantity, int(quantity), precision_digits=rounding) != 0:
            #         quantity = 0
            try:
                with self.env.cr.savepoint():
                    if not float_is_zero(
                        quantity, precision_rounding=self.product_id.uom_id.rounding
                    ):
                        # TODO: check and confirm that only one quant should be returned here
                        quants = self.env["stock.quant"]._update_reserved_quantity(
                            self.product_id,
                            location_id,
                            quantity,
                            lot_id=line.lot_id,
                            strict=True,
                        )
            except UserError:
                quantity = 0
            if quants:
                reserved_qty_diff = quants[0][1]  # newly reserved qty
                reserved_qty = line.product_qty + reserved_qty_diff
                uom_quantity = self.product_id.uom_id._compute_quantity(
                    reserved_qty, line.product_uom_id, rounding_method="HALF-UP"
                )
                uom_quantity = float_round(uom_quantity, precision_digits=rounding)
                uom_quantity_back_to_product_uom = line.product_uom_id._compute_quantity(
                    uom_quantity, self.product_id.uom_id, rounding_method="HALF-UP"
                )
                if (
                    float_compare(
                        reserved_qty,
                        uom_quantity_back_to_product_uom,
                        precision_digits=rounding,
                    )
                    == 0
                ):
                    line.with_context(
                        bypass_reservation_update=True
                    ).product_uom_qty = uom_quantity
                    # line.uom_qty_to_reserve = 0
            taken_quantity += quantity
        return taken_quantity

    def action_assign_component(self):
        """Logic is taken from the standard _action_assign() method but the
        difference is that we do try generating stock move line records here.
        Instead, we try to update the reservation of the stock according to
        the manually input stock move lines.
        """
        assigned_moves = self.env["stock.move"]
        partially_available_moves = self.env["stock.move"]
        # Read the `reserved_availability` field of the moves out of the loop to prevent unwanted
        # cache invalidation when actually reserving the move.
        reserved_availability = {move: move.reserved_availability for move in self}
        roundings = {move: move.product_id.uom_id.rounding for move in self}
        # for move in self.filtered(lambda m: m.state in ["confirmed", "partially_available"]):
        for move in self:
            if (
                move.product_id.tracking != "lot"
                or move.product_id.type == "consu"
                or move.state not in ["confirmed", "partially_available", "assigned"]
                or move.location_id.should_bypass_reservation()
                or move.move_orig_ids
                or move.procure_method == "make_to_order"
            ):
                continue
            rounding = roundings[move]
            missing_reserved_uom_quantity = (
                move.product_uom_qty - reserved_availability[move]
            )
            missing_reserved_quantity = move.product_uom._compute_quantity(
                missing_reserved_uom_quantity,
                move.product_id.uom_id,
                rounding_method="HALF-UP",
            )
            taken_quantity = move._update_reserved_quantity_component(
                # move.location_id, strict=False
                move.location_id
            )
            # TODO: should the case of taken_quantity being zero allowed?
            if float_is_zero(taken_quantity, precision_rounding=rounding):
                continue
            if (
                float_compare(
                    missing_reserved_quantity,
                    taken_quantity,
                    precision_rounding=rounding,
                )
                == 0
            ):
                assigned_moves |= move
            else:
                partially_available_moves |= move
        partially_available_moves.write({"state": "partially_available"})
        assigned_moves.write({"state": "assigned"})

    @api.multi
    def action_create_move_lines(self):
        self.ensure_one()
        move_line_vals_list = []
        for quant in self.quant_ids:
            vals = self._prepare_move_line_vals(reserved_quant=quant)
            vals = dict(vals, quant_id=quant.id, lot_id=quant.lot_id.id)
            move_line_vals_list.append(vals)
        self.env["stock.move.line"].create(move_line_vals_list)
        self.write({"quant_ids": [(5, 0, 0)]})

    @api.multi
    def action_view_stock_move_lines(self):
        # This method is expected to be used for component moves of a
        # production.
        self.ensure_one()
        action = self.env.ref(
            "mrp_production_manual_reserve.act_product_reserving_stock_move_open"
        ).read()[0]
        action["context"] = {
            "default_move_id": self.id,
            "default_product_id": self.product_id.id,
            "default_product_uom_id": self.product_uom.id,
            "default_location_id": self.location_id.id,
            "default_location_dest_id": self.location_dest_id.id,
        }
        action["domain"] = [
            ("product_id", "=", self.product_id.id),
            ("move_id", "=", self.id),
        ]
        return action
