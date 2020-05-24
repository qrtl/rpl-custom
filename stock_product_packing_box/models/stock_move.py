# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_packing_coefficient(self):
        res = 0.0
        for move in self:
            quantity = (
                move.reserved_availability
                if move.picking_id.box_calc_type == "reserved_qty"
                else move.product_uom_qty
            )
            res += move.product_id.packing_coefficient * quantity
        return res
