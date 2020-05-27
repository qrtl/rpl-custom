# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    rakushisu_order_id = fields.Char(
        "Order ID (Rakushisu)", compute="_compute_rakushisu_order_id"
    )
    rakushisu_status = fields.Char(string="Status (Rakushisu)")

    @api.multi
    def _compute_rakushisu_order_id(self):
        for order in self:
            order.rakushisu_order_id = order.name.replace("SO", "")

    def export_order_csv(self):
        orders = self.env["sale.order"].search([("state", "in", ("done", "sale"))])
        return self.env.ref("sale_order_export_rpl.sale_order_csv").report_action(
            orders.ids
        )

    def export_order_line_csv(self):
        orders = self.env["sale.order"].search([("state", "in", ("done", "sale"))])
        return self.env.ref("sale_order_export_rpl.sale_order_line_csv").report_action(
            orders.ids
        )
