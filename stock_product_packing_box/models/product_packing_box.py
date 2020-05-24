# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class ProductPackingBox(models.Model):
    _name = "product.packing.box"

    name = fields.Char(required=True,)
    packing_coefficient = fields.Float(
        required=True, digits=dp.get_precision("Product Coefficient"),
    )
    box_length = fields.Float("Length",)
    box_width = fields.Float("Width",)
    box_height = fields.Float("Height",)
    box_dest_id = fields.Many2one(
        "product.packing.box",
        string="Target Box",
        help="The box set here will be proposed instead.",
    )
    is_for_liquid = fields.Boolean()

    def _convert_packing_box(self, min_box):
        self.ensure_one()
        res = self.box_dest_id if self.box_dest_id else self
        if min_box and self.packing_coefficient < min_box.packing_coefficient:
            res = min_box
        return res
