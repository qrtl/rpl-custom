# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    line_packing_coefficient = fields.Float(
        compute="_compute_line_packing_coefficient",
        store=True,
    )

    @api.multi
    @api.depends("picking_id.packing_quantity", "reserved_availability")
    def _compute_line_packing_coefficient(self):
        for move in self:
            quantity = move.reserved_availability if move.picking_id.packing_quantity == 'reserved_qty' else move.product_uom_qty
            move.line_packing_coefficient = move.product_id.packing_coefficient * quantity
