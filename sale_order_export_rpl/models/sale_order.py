# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    luxis_order_id = fields.Char(
        "Order ID (luxis)",
        compute="_compute_luxis_order_id"
    )
    luxis_status = fields.Char(string='Status (luxis)')


    @api.multi
    def _compute_luxis_order_id(self):
        for order in self:
            order.luxis_order_id = order.name.replace("SO", "")
