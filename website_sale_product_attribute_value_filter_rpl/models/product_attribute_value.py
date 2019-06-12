# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    allowed_country_group_ids = fields.Many2many(
        'res.country.group',
        'res_country_group_attribute_value_rel',
        'attribute_value_id', 'res_country_group_id',
        string='Country Groups',
        help='If specified, the attribute value will only be visible to '
             'customers from the countries in the specified group(s).',
    )
