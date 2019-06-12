# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, SUPERUSER_ID


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _is_combination_possible(self, combination, parent_combination=None):
        res = super(ProductTemplate, self)._is_combination_possible(
            combination, parent_combination)
        if res:
            allowed_country_list = []
            country_lists = self._get_allowed_countries(combination)
            if country_lists:
                for country_list in country_lists:
                    allowed_country_list = list(set(allowed_country_list
                    ).intersection(country_list)) if allowed_country_list \
                    else country_list
                    # this is the conflicting case between the lists of
                    # allowed countries
                    if not allowed_country_list:
                        return False
                partner = self.env['res.users'].browse(
                    self._context.get('uid', SUPERUSER_ID)
                ).partner_id.commercial_partner_id
                # we assume that country is always set for customers
                if partner.country_id and not partner.country_id.id in \
                    allowed_country_list:
                    return False
        return res

    def _get_allowed_countries(self, combination):
        res = []
        for ptav in combination:
            if ptav.product_attribute_value_id.allowed_country_group_ids:
                groups = ptav.product_attribute_value_id.\
                    allowed_country_group_ids
                country_ids = []
                for group in groups:
                    country_ids += group.country_ids.ids
                res.append(list(set(country_ids)))
        return res
