# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    report_footer_custom = fields.Html(
        "Report Footer Information",
        help="To reset the value, please update the source and translations strings of the translation record.",
        translate=True,
        sanitize=False,
    )
