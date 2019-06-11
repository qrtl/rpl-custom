# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestWebsiteSaleProductAttributeValueFilterRpl(common.TransactionCase):

    def setUp(self):
        super(TestWebsiteSaleProductAttributeValueFilterRpl, self).setUp()
        self.demo_user = self.env.ref('base.demo_user0')
        self.test_product_template = self.env.ref(
            'product.product_product_11_product_template')
        self.test_product_variant_steel = self.env.ref(
            'product.product_product_11')
        self.steel_attribute_value = self.env.ref(
            'product.product_attribute_value_1')
        self.product_template_steel_attribute_value = self.env.ref(
            'sale.product_template_attribute_value_4')
        self.europe_country_group = self.env.ref('base.europe')
        self.japan = self.env.ref('base.jp')
        self.belgium = self.env.ref('base.be')
        self.context = {'uid': self.demo_user.id}

    def test_00_no_constriants(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write({
            'country_id': False
        })
        self.steel_attribute_value.sudo().write({
            'allowed_country_group_ids': False
        })
        self.assertEqual(self.test_product_template.with_context(
            self.context)._is_combination_possible(self.product_template_steel_attribute_value), True)

    def test_01_partner_with_country(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write({
            'country_id': self.belgium.id
        })
        self.steel_attribute_value.sudo().write({
            'allowed_country_group_ids': False
        })
        self.assertEqual(self.test_product_template.with_context(
            self.context)._is_combination_possible(self.product_template_steel_attribute_value), True)

    def test_02_partner_with_country_in_attribute_country_group(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write({
            'country_id': self.belgium.id
        })
        self.steel_attribute_value.sudo().write({
            'allowed_country_group_ids': [(6, 0, [self.europe_country_group.id])]
        })
        self.assertEqual(self.test_product_template.with_context(
            self.context)._is_combination_possible(self.product_template_steel_attribute_value), True)

    def test_03_partner_with_country_outside_attribute_country_group(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write({
            'country_id': self.japan.id
        })
        self.steel_attribute_value.sudo().write({
            'allowed_country_group_ids': [(6, 0, [self.europe_country_group.id])]
        })
        self.assertEqual(self.test_product_template.with_context(
            self.context)._is_combination_possible(self.product_template_steel_attribute_value), False)

    def test_04_attribute_country_group(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write({
            'country_id': False
        })
        self.steel_attribute_value.sudo().write({
            'allowed_country_group_ids': [(6, 0, [self.europe_country_group.id])]
        })
        self.assertEqual(self.test_product_template.with_context(
            self.context)._is_combination_possible(self.product_template_steel_attribute_value), True)
