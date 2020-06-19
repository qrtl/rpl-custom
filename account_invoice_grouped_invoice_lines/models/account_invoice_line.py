# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discounted_price_unit = fields.Float(
        string="Discount Price Unit",
        compute="_compute_discounted_price_unit",
        store=True,
    )

    @api.multi
    @api.depends("discount", "price_unit")
    def _compute_discounted_price_unit(self):
        for invoice_line in self:
            invoice_line.discounted_price_unit = invoice_line.price_unit * (
                1 - (invoice_line.discount or 0.0) / 100
            )
