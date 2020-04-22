# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    packing_coefficient = fields.Float(
        "Packing Coefficient"
    )
    product_packing_divison_id = fields.Many2one(
        'product.packing.division',
        string='Packing Box Division'
    )
