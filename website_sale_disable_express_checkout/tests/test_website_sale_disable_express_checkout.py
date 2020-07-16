# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class TestUi(odoo.tests.HttpCase):
    def setUp(self):
        super(TestUi, self).setUp()

    def test_disable_express_checkout(self):
        self.website = self.env["website"].browse(1)
        partner_id = self.env.ref("base.partner_demo_portal")
        self._create_so(partner_id.id)
        partner_id.write({"street": "", "city": ""})
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].run('website_sale_disable_express_checkout')",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'"
            "].tours.website_sale_disable_express_checkout.ready",
            login="portal",
        )

        # Compare the Partner Address values which is
        # enter through website address page.
        self.assertEqual(
            partner_id.street,
            "Test Street 1",
            "Partner Address Street field does not match with value.",
        )
        self.assertEqual(
            partner_id.city,
            "Test City",
            "Partner Address city field does not match with value.",
        )

    def _create_so(self, partner_id=None):
        return self.env["sale.order"].create(
            {
                "partner_id": partner_id,
                "website_id": self.website.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env["product.product"]
                            .create({"name": "Product A", "list_price": 100})
                            .id,
                            "name": "Product A",
                        },
                    )
                ],
            }
        )
