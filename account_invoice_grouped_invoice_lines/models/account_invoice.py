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
        # display_type "line_note" and "line_section" are excluded
        invoice_lines = self.invoice_line_ids.filtered(
            lambda l: not l.display_type
        ).sorted(key=lambda x: (x.product_id.name, x.name, x.price_unit, x.discount,))
        for _key, group in groupby(
            invoice_lines, lambda x: (x.product_id, x.price_unit, x.discount)
        ):
            line_recs = list(group)
            group_invoice_lines.append(
                {
                    "name": line_recs[0].name,
                    "product": line_recs[0].product_id,
                    "price_unit": line_recs[0].price_unit,
                    "discount": line_recs[0].discount or 0.0,
                    "quantity": sum(rec.quantity for rec in line_recs),
                    "price_subtotal": sum(rec.price_subtotal for rec in line_recs),
                }
            )
        return group_invoice_lines
