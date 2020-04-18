# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    public_category_ids = fields.Many2many(
        "product.public.category", string="eCommerce Categories to Hide",
    )
