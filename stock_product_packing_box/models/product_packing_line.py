# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductPackingLine(models.Model):
    _name = "product.packing.line"

    picking_id = fields.Many2one("stock.picking", string="Stock Picking",)
    packing_box_id = fields.Many2one("product.packing.box", string="Packing Box",)
    box_quantity = fields.Integer(string="No. of Boxes",)
