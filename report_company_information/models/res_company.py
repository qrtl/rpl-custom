# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_information = fields.Html(
        "Company Information",
        help="Company information that should show in report footer when set.",
        translate=True,
        sanitize=False,
    )
