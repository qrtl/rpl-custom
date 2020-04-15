# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.public.category"

    partner_ids = fields.Many2many("res.partner", string="Partners")
