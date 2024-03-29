# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import odoo.tests

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteSaleForm


@odoo.tests.tagged("post_install", "-at_install")
class TestUi(odoo.tests.HttpCase):
    def setUp(self):
        super(TestUi, self).setUp()
        self.website = self.env["website"].browse(1)
        self.WebsiteSaleController = WebsiteSaleForm()

    def test_01_website_sale_comment(self):
        # Enable Extra Step option from Customize Menu
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].run("
            "'enable_extra_step_setting')",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].tours.enable_extra_step_setting.ready",
            login="admin",
        )
        partner = self.env.ref("base.partner_demo_portal")
        partner.write({"street": "", "city": ""})

        # Checking the website comment flow
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].run('website_sale_comment_tour_sale')",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].tours.website_sale_comment_tour_sale.ready",
            login="portal",
        )

        partner_id = self.env.ref("base.partner_demo_portal").id
        sale_order = self.env["sale.order"].search(
            [("partner_id", "=", partner_id)], limit=1
        )

        # Compare the SaleOrder Note2 Value which is create by tour test-case
        self.assertEqual(
            sale_order.note1,
            "<p>Test Feedback Comment</p>",
            "Sale Order Note1 does not Match with the value.",
        )

    def test_02_input_comment_order_note2(self):
        partner = self.env.user.partner_id
        so = self._create_so(partner.id)
        with MockRequest(
            self.env, website=self.website, sale_order_id=so.id
        ) as request:
            # Note: if you face this kind of errors
            # during the using of MockRequest.
            # ` AttributeError: 'NoneType' object has no attribute 'environ' `
            # to fix above error added this headers and environ in request.
            httprequest = request.httprequest
            httprequest.update({"headers": {"environ": {}}})
            # Update the httprequest with request Object
            request.update({"httprequest": httprequest})
            values = {"Give us your feedback": "test-comment"}

            # Call the Controller Method for pass the feedback values.
            # `website_form_saleorder`
            self.WebsiteSaleController.website_form_saleorder(**values)
            self.assertEqual(
                so.note1, "<p>test-comment</p>",
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
