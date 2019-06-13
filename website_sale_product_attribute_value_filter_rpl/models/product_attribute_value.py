# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, SUPERUSER_ID


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    allowed_country_group_ids = fields.Many2many(
        'res.country.group',
        'res_country_group_attribute_value_rel',
        'attribute_value_id', 'res_country_group_id',
        string='Country Groups',
        help='If specified, the attribute value will only be visible to '
             'customers from the countries in the specified group(s) in '
             'e-commerce.',
    )

    @api.multi
    def in_country_group_constraint(self):
        allowed_country_list = []
        country_lists = self._get_allowed_countries()
        if country_lists:
            for country_list in country_lists:
                allowed_country_list = list(set(allowed_country_list).\
                    intersection(country_list)) if allowed_country_list \
                        else country_list
                # this is the conflicting case between the lists of
                # allowed countries
                if not allowed_country_list:
                    return True
            partner = self.env['res.users'].sudo().browse(
                self._context.get('uid', SUPERUSER_ID)
            ).partner_id.commercial_partner_id
            # we assume that country is always set for customers
            if partner.country_id and not partner.country_id.id in \
                    allowed_country_list:
                return True
        return False

    @api.multi
    def _get_allowed_countries(self):
        res = []
        for pav in self:
            if pav.allowed_country_group_ids:
                groups = pav.allowed_country_group_ids
                country_ids = []
                for group in groups:
                    country_ids += group.country_ids.ids
                res.append(list(set(country_ids)))
        return res
