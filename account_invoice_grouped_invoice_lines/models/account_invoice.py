# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from itertools import groupby

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def report_grouped_invoice_lines(self):
        self.ensure_one()
        group_invoice_lines = []
        invoice_lines = self.invoice_line_ids.filtered(
            lambda l: l.price_subtotal > 0.0
        ).sorted(
            key=lambda x: (
                x.product_id.default_code,
                x.product_id.name,
                x.name,
                x.price_unit,
                x.discount,
            )
        )
        for _key, group in groupby(
            invoice_lines, lambda x: (x.product_id, x.price_unit, x.discount)
        ):
            line_recs = list(group)
            group_invoice_lines.append(
                {
                    "product": line_recs[0].product_id,
                    "price_unit": line_recs[0].price_unit
                    * (1 - (line_recs[0].discount or 0.0) / 100),
                    "quantity": sum(rec.quantity for rec in line_recs),
                    "price_subtotal": sum(rec.price_subtotal for rec in line_recs),
                }
            )
        return group_invoice_lines
