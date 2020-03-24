# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    label_ref = fields.Char(
        "Label Reference",
        help="The value set here will be used as 'REF' in product label " "print.",
    )
