# Copyright 2019-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    company_chop = fields.Binary("Company Chop Image", attachment=True,)
    fax = fields.Char("Fax")
    ceo = fields.Char("Representative Director")
    bank_info = fields.Text("Bank Information", translate=True)
