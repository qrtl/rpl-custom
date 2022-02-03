# Copyright 2021-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Only one selection is expected per website.
    acquirer_ids = fields.Many2many(
        "payment.acquirer",
        string="Acquirers",
        help="Select the direct debit acquirers as necessary.",
    )
