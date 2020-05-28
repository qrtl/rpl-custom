# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    rakushisu_item_id = fields.Char("Item ID (rakushisu)")
    rakushisu_product_id = fields.Char("Product ID (rakushisu)")