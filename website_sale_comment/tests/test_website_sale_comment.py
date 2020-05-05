# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common, tagged

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale_comment.controllers.main import WebsiteSale


@tagged("post_install", "-at_install")
class TestWebsiteSaleComment(common.TransactionCase):
    def setUp(self):
        super(TestWebsiteSaleComment, self).setUp()
        self.website = self.env["website"].browse(1)
        self.WebsiteSaleController = WebsiteSale()

    # TEST WEBSITE SALE COMMENT
    def test_01_create_website_sale_comment(self):
        partner = self.env.user.partner_id
        so = self._create_so(partner.id)
        with MockRequest(self.env, website=self.website, sale_order_id=so.id):
            note2 = "<p>test-comment</p>"
            self.WebsiteSaleController.order_notes(note2=note2, **{})
            self.assertEqual(so.note2, note2, "Test-Comment Added to SaleOrder")

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
