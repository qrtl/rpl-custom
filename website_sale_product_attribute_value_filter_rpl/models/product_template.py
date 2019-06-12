# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _is_combination_possible(self, combination, parent_combination=None):
        res = super(ProductTemplate, self)._is_combination_possible(
            combination, parent_combination)
        if res:
            if combination.mapped('product_attribute_value_id').\
                in_country_group_constraint():
                return False
        return res
