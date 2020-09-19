# Copyright 2019-2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_chop = fields.Binary("Company Chop Image", attachment=True,)
    fax = fields.Char("Fax")
    ceo = fields.Char("Representative Director")
