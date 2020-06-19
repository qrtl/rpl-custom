# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from itertools import groupby


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def report_grouped_invoice_lines(self):
        self.ensure_one()
        group_invoice_lines = []
        invoice_lines = self.invoice_line_ids.filtered(lambda l: l.price_subtotal > 0.0).sorted(key=lambda x: (x.product_id.id, x.discounted_price_unit))
        for _key, group in groupby(invoice_lines, lambda x: (x.product_id, x.discounted_price_unit)):
            lines_recs = list(group)
            group_invoice_lines.append(
                {
                    "product": lines_recs[0].name,
                    "price_unit": lines_recs[0].discounted_price_unit,
                    "quantity": sum(l.quantity for l in lines_recs),
                    "price_subtotal": sum(l.price_subtotal for l in lines_recs),
                }
            )
        return group_invoice_lines
