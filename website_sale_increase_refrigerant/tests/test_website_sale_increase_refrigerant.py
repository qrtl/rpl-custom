# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import odoo.tests

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteSaleForm


@odoo.tests.tagged("post_install", "-at_install")
class TestWebsiteSaleIncreaseRefrigerant(odoo.tests.HttpCase):
    def setUp(self):
        super(TestWebsiteSaleIncreaseRefrigerant, self).setUp()
        self.website = self.env["website"].browse(1)
        self.WebsiteSaleController = WebsiteSaleForm()

    def test_01_input_increase_refrigerant_order_note2(self):
        partner = self.env.user.partner_id
        so = self._create_so(partner.id)
        with MockRequest(
            self.env, website=self.website, sale_order_id=so.id
        ) as request:
            httprequest = request.httprequest
            httprequest.update({"headers": {"environ": {}}})
            # Update the httprequest with request Object
            request.update({"httprequest": httprequest})
            values = {"increase_refrigerant": True}

            # Call the Controller Method for pass the feedback values.
            # `website_form_saleorder`
            self.WebsiteSaleController.website_form_saleorder(**values)
            self.assertEqual(
                so.increase_refrigerant, True,
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
