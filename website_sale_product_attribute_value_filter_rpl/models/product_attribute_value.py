# Copyright 2019-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.multi
    def in_attribute_constraints(self):
        partner = (
            self.env["res.users"]
            .sudo()
            .browse(self._context.get("uid", SUPERUSER_ID))
            .partner_id.commercial_partner_id
        )
        partner_contraint, absolute_constraint = self._in_partner_constraint(partner)
        if absolute_constraint:
            return partner_contraint
        country_contraint, absolute_constraint = self._in_country_constraint(partner)
        if absolute_constraint:
            return country_contraint
        return self._in_country_group_constraint(partner)
        
    @api.multi
    def _in_partner_constraint(self, partner):
        # Return two boolean values, first value determines whether the
        # partner is being contrainted by the rules, the second value
        # represents whether it is an absolute constraint.
        allowed_partner_ids, unallowed_partner_ids = self._get_partner_contraints()
        if unallowed_partner_ids and partner.id in unallowed_partner_ids:
            return True, True
        if allowed_partner_ids and partner.id in allowed_partner_ids:
            return False, True
        return False, False
    
    @api.multi
    def _in_country_constraint(self, partner):
        # Return two boolean values, first value determines whether the
        # partner is being contrainted by the rules, the second value
        # represents whether it is an absolute constraint.
        allowed_country_ids, unallowed_country_ids = self._get_countries_contraints()
        if allowed_country_ids:
            if partner.country_id and partner.country_id.id in allowed_country_ids:
                return False, True
            if not partner.country_id:
                return True, True
        if unallowed_country_ids and partner.country_id and partner.country_id.id in unallowed_country_ids:
            return True, True
        return False, False

    @api.multi
    def _in_country_group_constraint(self, partner):
        allowed_country_ids, unallowed_country_ids = self._get_countries_group_contraints()
        if allowed_country_ids:
            if partner.country_id and partner.country_id.id in allowed_country_ids:
                return False
            if not partner.country_id:
                return True
        if unallowed_country_ids and partner.country_id and partner.country_id.id in unallowed_country_ids:
            return True
        return False

    @api.multi
    def _get_partner_contraints(self):
        rules = self._get_permission_rules()
        allowed_partner_ids = rules.mapped('allowed_partner_ids').ids
        unallowed_partner_ids = rules.mapped('unallowed_partner_ids').ids
        return allowed_partner_ids, unallowed_partner_ids

    @api.multi
    def _get_countries_contraints(self):
        rules = self._get_permission_rules()
        allowed_country_ids = rules.mapped('allowed_country_ids').ids
        unallowed_country_ids = rules.mapped('unallowed_country_ids').ids
        return allowed_country_ids, unallowed_country_ids

    @api.multi
    def _get_countries_group_contraints(self):
        rules = self._get_permission_rules()
        allowed_country_ids = rules.mapped('allowed_country_group_ids').mapped('country_ids').ids
        unallowed_country_ids = rules.mapped('unallowed_country_group_ids').mapped('country_ids').ids
        return allowed_country_ids, unallowed_country_ids

    @api.multi
    def _get_permission_rules(self):
        rules = self.env['product.attribute.value.permission'].search([
            ('product_attribute_value_id', 'in', self.ids)
        ])
        return rules
