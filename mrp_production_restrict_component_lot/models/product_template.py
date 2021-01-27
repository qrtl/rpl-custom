# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    lot_restriction = fields.Boolean(help="Select this in case lot restriction should be applied to this product (as a component) in manufacturing orders.")
