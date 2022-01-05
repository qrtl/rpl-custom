# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    qty_total = fields.Float(
        compute="_compute_qty_total", store=True, track_visibility="onchange"
    )

    @api.depends("order_line.product_uom_qty")
    def _compute_qty_total(self):
        for order in self:
            order.qty_total = sum(order.order_line.mapped("product_uom_qty"))
