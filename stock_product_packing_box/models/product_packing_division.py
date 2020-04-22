# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductPackingDivision(models.Model):
    _name = "product.packing.division"

    name = fields.Char(
        "Division Name"
    )
