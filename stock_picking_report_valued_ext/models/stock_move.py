# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        if self.sale_line_id and self.sale_line_id.order_id:
            vals["delivery_price"] = sum(
                [
                    line.price_reduce_taxinc
                    for line in self.sale_line_id.order_id.order_line
                    if line.is_delivery
                ]
            )
        return vals
