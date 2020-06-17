# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import html2text

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    rakushisu_order_id = fields.Char(
        "Order ID (Rakushisu)", compute="_compute_rakushisu_order_id"
    )
    rakushisu_status = fields.Char(string="Status (Rakushisu)")
    no_export = fields.Boolean(string="Exclude From Export")
    note2_export = fields.Char(
        string="Bottom Comment (Export)", compute="_compute_note2_export", store=True,
    )

    @api.multi
    def _compute_rakushisu_order_id(self):
        for order in self:
            order.rakushisu_order_id = order.name.replace("SO", "")

    def export_order_csv(self):
        domain = self._get_export_domain()
        orders = self.env["sale.order"].search(domain)
        return self.env.ref("sale_order_export_rpl.sale_order_csv").report_action(
            orders.ids
        )

    def export_order_line_csv(self):
        domain = self._get_export_domain()
        orders = self.env["sale.order"].search(domain)
        return self.env.ref("sale_order_export_rpl.sale_order_line_csv").report_action(
            orders.ids
        )

    def _get_export_domain(self):
        return [("state", "in", ("done", "sale")), ("no_export", "!=", True)]

    @api.multi
    @api.depends("note2")
    def _compute_note2_export(self):
        for order in self:
            if order.note2:
                order.note2_export = html2text.html2text(order.note2).replace("\n", " ")
