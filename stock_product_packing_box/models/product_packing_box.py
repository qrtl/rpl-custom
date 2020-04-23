# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductPackingBox(models.Model):
    _name = "product.packing.box"

    name = fields.Char("Box Name", required=True,)
    packing_coefficient = fields.Float("Packing Coefficient", required=True,)
    box_length = fields.Float("Length",)
    box_width = fields.Float("Width",)
    box_height = fields.Float("Height",)
    product_packing_divison_id = fields.Many2one(
        "product.packing.division", string="Packing Box Division", required=True
    )
    uom_id = fields.Many2one("uom.uom", string="Package Unit", required=True)
    dimension_uom_id = fields.Many2one("uom.uom", string="Dimension unit")
    exception_product_ids = fields.Many2many("product.product", string="Exception Products")
