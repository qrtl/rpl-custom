# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_round, float_is_zero

class StockMove(models.Model):
    _inherit = "stock.move"

    qty_to_reserve = fields.Float(
        'Quantity to Reserve', compute='_compute_qty_to_reserve',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True,
        help="Quantity that is expected to be reserved for this move."
    )

    @api.multi
    @api.depends("move_line_ids.qty_to_reserve")
    def _compute_qty_to_reserve(self):
        result = {data['move_id'][0]: data['qty_to_reserve'] for data in 
            self.env['stock.move.line'].read_group([('move_id', 'in', self.ids)], ['move_id', "qty_to_reserve"], ['move_id'])}
        for rec in self:
            qty_to_reserve = rec.product_id.uom_id._compute_quantity(result.get(rec.id, 0.0), rec.product_uom, rounding_method='HALF-UP')
            if rec.product_qty >= rec.reserved_availability + qty_to_reserve:
                rec.qty_to_reserve = qty_to_reserve
            else:
                raise UserError(_("You are trying to reserve more that needed."))

    def _update_reserved_quantity_component(self, location_id, strict=True):
        """Unlike the standard method _update_reserved_quantity(), we will not
        create move lines here. We will just try updating reserved quantities
        of quants to keep consistency between existing move lines and quants.
        """
        self.ensure_one()
        taken_quantity = 0
        for line in self.move_line_ids:
            available_quantity = self.env['stock.quant']._get_available_quantity(line.product_id, line.location_id, line.lot_id)
            if available_quantity <= 0:
                continue
            quantity = min(line.qty_to_reserve, available_quantity)
            #TODO: should do something if need > available_quantity here?

            # `taken_quantity` is in the quants unit of measure. There's a possibility that the move's
            # unit of measure won't be respected if we blindly reserve this quantity, a common usecase
            # is if the move's unit of measure's rounding does not allow fractional reservation. We chose
            # to convert `taken_quantity` to the move's unit of measure with a down rounding method and
            # then get it back in the quants unit of measure with an half-up rounding_method. This
            # way, we'll never reserve more than allowed. We do not apply this logic if
            # `available_quantity` is brought by a chained move line. In this case, `_prepare_move_line_vals`
            # will take care of changing the UOM to the UOM of the product.
            if not strict:
                quantity_move_uom = self.product_id.uom_id._compute_quantity(quantity, self.product_uom, rounding_method='DOWN')
                quantity = self.product_uom._compute_quantity(quantity_move_uom, self.product_id.uom_id, rounding_method='HALF-UP')
            quants = []
            rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            #TODO: should we remove the case of serial?
            # if self.product_id.tracking == 'serial':
            #     if float_compare(quantity, int(quantity), precision_digits=rounding) != 0:
            #         quantity = 0
            try:
                with self.env.cr.savepoint():
                    if not float_is_zero(quantity, precision_rounding=self.product_id.uom_id.rounding):
                        #TODO: check and confirm that only one quant should be returned here
                        quants = self.env['stock.quant']._update_reserved_quantity(
                            self.product_id, location_id, quantity, lot_id=line.lot_id,
                            strict=strict
                        )
            except UserError:
                quantity = 0
            if quants:
                reserved_qty = quants[0][1]
                uom_quantity = self.product_id.uom_id._compute_quantity(reserved_qty, line.product_uom_id, rounding_method='HALF-UP')
                uom_quantity = float_round(uom_quantity, precision_digits=rounding)
                uom_quantity_back_to_product_uom = line.product_uom_id._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
            if float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
                line.with_context(bypass_reservation_update=True).product_uom_qty = uom_quantity
            taken_quantity += quantity
        return taken_quantity

    def _action_assign_component(self):
        """Logic is taken from the standard _action_assign() method but the
        difference is that we do try generating stock move line records here.
        Instead, we try to update the reservation of the stock according to
        the manually input stock move lines.
        """
        assigned_moves = self.env['stock.move']
        partially_available_moves = self.env['stock.move']
        # Read the `reserved_availability` field of the moves out of the loop to prevent unwanted
        # cache invalidation when actually reserving the move.
        reserved_availability = {move: move.reserved_availability for move in self}
        roundings = {move: move.product_id.uom_id.rounding for move in self}
        # for move in self.filtered(lambda m: m.state in ["confirmed", "partially_available"]):
        for move in self:
            if move.product_id.tracking != "lot" or move.product_id.type == "consu" or move.state not in ["confirmed", "partially_available"] or move.location_id.should_bypass_reservation() or move.move_orig_ids or move.procure_method == "make_to_order":
                continue
            rounding = roundings[move]
            missing_reserved_uom_quantity = move.product_uom_qty - reserved_availability[move]
            missing_reserved_quantity = move.product_uom._compute_quantity(
                missing_reserved_uom_quantity,
                move.product_id.uom_id,
                rounding_method="HALF-UP"
            )
            # if move.location_id.should_bypass_reservation()\
            #         or move.product_id.type == 'consu':
            #     pass
            # elif not move.move_orig_ids:
            #     if move.procure_method == 'make_to_order':
            #         continue
            taken_quantity = move._update_reserved_quantity_component(move.location_id, strict=False)
            #TODO: should the case of taken_quantity being zero allowed?
            if float_is_zero(taken_quantity, precision_rounding=rounding):
                continue
            if float_compare(missing_reserved_quantity, taken_quantity, precision_rounding=rounding) == 0:
                assigned_moves |= move
            else:
                partially_available_moves |= move
        partially_available_moves.write({'state': 'partially_available'})
        assigned_moves.write({'state': 'assigned'})

    # @api.multi
    # @api.depends('move_line_ids.product_qty')
    # def _compute_reserved_availability(self):
    #     super()._compute_reserved_availability()
    #     for rec in self:
    #         if rec.reserved_availability:
    #             if rec.reserved_availability < rec.product_uom_qty:
    #                 rec.write({"state": "partially_available"})
    #             elif rec.reserved_availability < rec.product_uom_qty:
    #                 rec.write({"state": "assigned"})

    # def write(self, vals):
    #     res = super().write(vals)
    #     for move in self:
    #         if move.reserved_availability:
    #             if move.reserved_availability < move.product_uom_qty and move.state != "partially_available":
    #                 move.write({"state": "partially_available"})
    #             elif move.reserved_availability == move.product_uom_qty and move.state != "assigned":
    #                 move.write({"state": "assigned"})
    #     return res

    @api.multi
    def action_view_stock_move_lines(self):
        # This method is expected to be used for component moves of a
        # production.
        self.ensure_one()
        action = self.env.ref(
            "mrp_production_stock_move_line_link.act_product_reserving_stock_move_open"
        ).read()[0]
        action["context"] = {
            "default_move_id": self.id,
            "default_product_id": self.product_id.id,
            "default_product_uom_id": self.product_uom.id,
            "default_location_id": self.location_id.id,
            "default_location_dest_id": self.location_dest_id.id,
        }
        action['domain'] = [
            ("product_id", "=", self.product_id.id),
            ("move_id", "=", self.id),
        ]
        return action
