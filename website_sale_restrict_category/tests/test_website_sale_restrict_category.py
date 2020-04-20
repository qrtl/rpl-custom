# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestWebsiteSaleRestrictCategory(common.TransactionCase):
    def setUp(self):
        super(TestWebsiteSaleRestrictCategory, self).setUp()
        self.test_user_1 = self.env["res.users"].create(
            {
                "login": "testuser1",
                "partner_id": self.env["res.partner"]
                .create({"name": "Test User 1"})
                .id,
                "groups_id": [(4, self.env.ref("base.group_portal").id, 0)],
            }
        )
        self.test_user_2 = self.env["res.users"].create(
            {
                "login": "testuser2",
                "partner_id": self.env["res.partner"]
                .create({"name": "Test User 2"})
                .id,
                "groups_id": [(4, self.env.ref("base.group_portal").id, 0)],
            }
        )
        self.test_category_1 = self.env["product.public.category"].create(
            {"name": "Category 1"}
        )
        self.test_category_2 = self.env["product.public.category"].create(
            {"name": "Category 2", "parent_id": self.test_category_1.id}
        )
        self.test_category_3 = self.env["product.public.category"].create(
            {"name": "Category 2", "parent_id": self.test_category_1.id}
        )
        self.test_category_4 = self.env["product.public.category"].create(
            {"name": "Category 3", "parent_id": self.test_category_2.id}
        )
        self.test_product = self.env.ref("product.product_product_3")
        self.website = self.env["website"].browse(1)

    def test_00_get_offsprings(self):
        self.assertEqual(
            self.test_category_1.get_offsprings(),
            self.test_category_1
            + self.test_category_2
            + self.test_category_3
            + self.test_category_4,
        )
        self.assertEqual(
            self.test_category_2.get_offsprings(),
            self.test_category_2 + self.test_category_4,
        )
        self.assertEqual(self.test_category_4.get_offsprings(), self.test_category_4)

    def test_01_sale_product_domain(self):
        product = self.env["product.template"]
        base_domain = [("sale_ok", "=", True)]
        # Search without any restricted category
        sale_product_domain_products = product.search(
            self.website.sudo(self.test_user_1.id).sale_product_domain()
        )
        all_products = product.search(base_domain)
        self.assertEqual(sale_product_domain_products, all_products)
        # Assign test_category_4 to test_product and to test_user_1,
        # test_product should be restricted from test_user_1
        self.test_product.public_categ_ids = [(6, 0, [self.test_category_4.id])]
        self.test_user_1.partner_id.public_category_ids = [
            (4, self.test_category_4.id, 0)
        ]
        sale_product_domain_products = product.search(
            self.website.sudo(self.test_user_1.id).sale_product_domain()
        )
        self.assertEqual(
            self.test_product.product_tmpl_id in sale_product_domain_products, False
        )
        # Check if test_product is visible to test_user_2
        sale_product_domain_products = product.search(
            self.website.sudo(self.test_user_2.id).sale_product_domain()
        )
        self.assertEqual(
            self.test_product.product_tmpl_id in sale_product_domain_products, True
        )
        # Assign non-restricted category_3 to test_product, test_product
        # should be visible to test_user_1
        self.test_product.public_categ_ids = [(4, self.test_category_3.id, 0)]
        self.test_user_1.partner_id.public_category_ids = [
            (4, self.test_category_4.id, 0)
        ]
        sale_product_domain_products = product.search(
            self.website.sudo(self.test_user_1.id).sale_product_domain()
        )
        self.assertEqual(
            self.test_product.product_tmpl_id in sale_product_domain_products, True
        )
