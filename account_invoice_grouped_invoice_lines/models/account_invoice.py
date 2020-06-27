# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from itertools import groupby

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def report_grouped_invoice_lines(self):
        self.ensure_one()
        grouped_lines = []

        # Firstly process invoice lines with product.
        lines = self.invoice_line_ids.filtered(lambda l: l.product_id).sorted(
            key=lambda x: (x.product_id.display_name, x.name, x.price_unit, x.discount)
        )
        for _key, group in groupby(
            lines, lambda x: (x.product_id.display_name, x.price_unit, x.discount)
        ):
            grouped_lines = self._update_grouped_lines(grouped_lines, group)

        # Secondly process invoice lines with no product.
        # display_type "line_note" and "line_section" should be excluded.
        lines = self.invoice_line_ids.filtered(
            lambda l: not l.product_id and not l.display_type
        ).sorted(key=lambda x: (x.name, x.price_unit, x.discount,))
        for _key, group in groupby(lines, lambda x: (x.name, x.price_unit, x.discount)):
            grouped_lines = self._update_grouped_lines(grouped_lines, group)
        return grouped_lines

    def _update_grouped_lines(self, grouped_lines, group):
        line_recs = list(group)
        grouped_lines.append(
            {
                "name": line_recs[0].name,
                "product": line_recs[0].product_id,
                "price_unit": line_recs[0].price_unit,
                "discount": line_recs[0].discount or 0.0,
                "quantity": sum(rec.quantity for rec in line_recs),
                "price_subtotal": sum(rec.price_subtotal for rec in line_recs),
            }
        )
        return grouped_lines
