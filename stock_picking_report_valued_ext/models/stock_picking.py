# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_price = fields.Monetary(
        string='Delivery Price',
        compute='_compute_delivery_price',
        store=True,
        readonly=False,
    )

    @api.multi
    @api.depends('sale_id')
    def _compute_delivery_price(self):
        for picking in self:
            if picking.sale_id:
                picking.delivery_price = sum(
                    [line.price_subtotal for line in picking.sale_id.order_line if line.is_delivery]
                )
