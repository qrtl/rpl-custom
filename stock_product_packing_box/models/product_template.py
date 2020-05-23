# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    packing_coefficient = fields.Float(
        "Packing Coefficient", digits=dp.get_precision("Product Coefficient")
    )
    has_liquid = fields.Boolean()
    min_box_id = fields.Many2one(
        "product.packing.box",
        help="When set, box proposal in picking will be done with boxes no "
        "smaller than the selected box.",
    )
