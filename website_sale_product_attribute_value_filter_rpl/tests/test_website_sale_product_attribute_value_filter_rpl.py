# Copyright 2019-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestWebsiteSaleProductAttributeValueFilterRpl(common.TransactionCase):
    def setUp(self):
        super(TestWebsiteSaleProductAttributeValueFilterRpl, self).setUp()
        self.demo_user = self.env.ref("base.demo_user0")
        self.public_user = self.env.ref("base.public_user")
        self.test_product_template = self.env.ref(
            "product.product_product_11_product_template"
        )
        self.test_product_variant_steel = self.env.ref("product.product_product_11")
        self.steel_attribute_value = self.env.ref("product.product_attribute_value_1")
        self.product_template_steel_attribute_value = self.env.ref(
            "sale.product_template_attribute_value_4"
        )
        self.europe_country_group = self.env.ref("base.europe")
        self.japan = self.env.ref("base.jp")
        self.belgium = self.env.ref("base.be")
        self.demo_context = {"uid": self.demo_user.id}
        self.public_context = {"uid": self.public_user.id}

    def test_00_no_rules(self):
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_01_allow_country_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": False}
        )
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'allowed_country_ids': [(4, self.belgium.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_02_unallow_country_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'unallowed_country_ids': [(4, self.belgium.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.japan.id}
        )
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_03_allow_country_group_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": False}
        )
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'allowed_country_group_ids': [(4, self.europe_country_group.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_04_unallow_country_group_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'unallowed_country_group_ids': [(4, self.europe_country_group.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.japan.id}
        )
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_05_allow_country_group_and_unallow_country_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'unallowed_country_ids': [(4, self.belgium.id, None)],
            'allowed_country_group_ids': [(4, self.europe_country_group.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )

    def test_06_allow_user_rule(self):
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'allowed_partner_ids': [(4, self.demo_user.partner_id.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )
        self.assertEqual(
            self.test_product_template.with_context(
                self.public_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_07_unallow_user_rule(self):
        self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'unallowed_partner_ids': [(4, self.demo_user.partner_id.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )
        self.assertEqual(
            self.test_product_template.with_context(
                self.public_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )

    def test_08_unallow_user_with_allow_country_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        rule = self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'allowed_country_group_ids': [(4, self.europe_country_group.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )
        rule.update({
            'unallowed_partner_ids': [(4, self.demo_user.partner_id.id, None)],
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )

    def test_09_allow_user_with_unallow_country_rule(self):
        self.demo_user.partner_id.commercial_partner_id.sudo().write(
            {"country_id": self.belgium.id}
        )
        rule = self.env['product.attribute.value.permission'].create({
            'product_id': self.test_product_variant_steel.id,
            'product_attribute_value_id': self.steel_attribute_value.id,
            'unallowed_country_group_ids': [(4, self.europe_country_group.id, None)]
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            False,
        )
        rule.update({
            'allowed_partner_ids': [(4, self.demo_user.partner_id.id, None)],
        })
        self.assertEqual(
            self.test_product_template.with_context(
                self.demo_context
            )._is_combination_possible(self.product_template_steel_attribute_value),
            True,
        )
