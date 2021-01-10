# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = "stock.move"

    allow_manual_reservation = fields.Boolean(compute="_compute_allow_manual_reservation")
    quant_ids = fields.Many2many("stock.quant", string="Quants")
    has_quant = fields.Boolean(compute="_compute_has_quant")
    should_reserve_stock = fields.Boolean(compute="_compute_should_reserve_stock")

    def _compute_allow_manual_reservation(self):
        for move in self:
            if not (
                move.product_id.tracking != "lot"
                or move.product_id.type == "consu"
                or move.state not in ["confirmed", "partially_available", "assigned"]
                or move.location_id.should_bypass_reservation()
                or move.move_orig_ids
                or move.procure_method == "make_to_order"
            ):
                move.allow_manual_reservation = True

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
            try:
                with self.env.cr.savepoint():
                    if not float_is_zero(
                        quantity, precision_rounding=self.product_id.uom_id.rounding
                    ):
                        quants = self.env["stock.quant"]._update_reserved_quantity(
                            self.product_id,
                            location_id,
                            quantity,
                            lot_id=line.lot_id,
                            strict=True,
                        )  # Only one quant should be returned here
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
            taken_quantity += quantity
        return taken_quantity

    def action_assign_component(self):
        """Relevant logic is taken from the standard _action_assign() method
        but the difference is that we do not try generating stock move line
        records here. Instead, we try to update the reservation of the stock
        according to the manually updated stock move lines.
        """
        #TODO: self.ensure_one()?
        # assigned_moves = self.env["stock.move"]
        # partially_available_moves = self.env["stock.move"]
        # Read the `reserved_availability` field of the moves out of the loop to prevent unwanted
        # cache invalidation when actually reserving the move.
        reserved_availability = {move: move.reserved_availability for move in self}
        roundings = {move: move.product_id.uom_id.rounding for move in self}
        for move in self:
            if not move.allow_manual_reservation:
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
                move.location_id
            )
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
                # assigned_moves |= move
                move.write({"state": "assigned"})
            else:
                # partially_available_moves |= move
                move.write({"state": "partially_available"})
        # partially_available_moves.write({"state": "partially_available"})
        # assigned_moves.write({"state": "assigned"})

    def action_create_move_lines(self):
        self.ensure_one()
        move_line_vals_list = []
        for quant in self.quant_ids:
            vals = self._prepare_move_line_vals(reserved_quant=quant)
            #TODO: add uom_qty_to_reserve in the dict
            vals = dict(vals, quant_id=quant.id, lot_id=quant.lot_id.id)
            move_line_vals_list.append(vals)
        self.env["stock.move.line"].create(move_line_vals_list)
        self.write({"quant_ids": [(5, 0, 0)]})
