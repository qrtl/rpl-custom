# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    luxis_item_id = fields.Integer("Item ID (luxis)")
    luxis_product_id = fields.Integer("Product ID (luxis)")
