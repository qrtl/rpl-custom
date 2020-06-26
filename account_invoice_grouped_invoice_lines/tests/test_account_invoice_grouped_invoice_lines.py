# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestAccountInvoceGroupedInvoiceLines(common.TransactionCase):
    def setUp(self):
        super(TestAccountInvoceGroupedInvoiceLines, self).setUp()
        self.product1 = self.env.ref("product.product_product_7")
        self.product2 = self.env.ref("product.product_product_8")
        account_type = self.env.ref("account.data_account_type_revenue")
        self.customer = self.env.ref("base.res_partner_2")
        self.account = self.env["account.account"].search(
            [("user_type_id", "=", account_type.id)], limit=1
        )
        self.journal = self.env["account.journal"].create(
            {"name": "Sale journal - Test", "code": "SJ-TT", "type": "sale"}
        )

    def test_group_invoice_lines(self):
        invoice_lines1 = [
            (
                0,
                False,
                {
                    "name": self.product1.display_name,
                    "product_id": self.product1.id,
                    "quantity": 1,
                    "uom_id": self.product1.uom_id.id,
                    "price_unit": 100,
                    "account_id": self.customer.property_account_receivable_id.id,
                },
            ),
            (
                0,
                False,
                {
                    "name": self.product1.display_name,
                    "product_id": self.product1.id,
                    "quantity": 2,
                    "uom_id": self.product1.uom_id.id,
                    "price_unit": 100,
                    "account_id": self.customer.property_account_receivable_id.id,
                },
            ),
            (
                0,
                False,
                {
                    "name": self.product2.display_name,
                    "product_id": self.product2.id,
                    "quantity": 3,
                    "uom_id": self.product2.uom_id.id,
                    "price_unit": 100,
                    "account_id": self.customer.property_account_receivable_id.id,
                },
            ),
        ]
        invoice1 = self.env["account.invoice"].create(
            {
                "partner_id": self.customer.id,
                "type": "out_invoice",
                "date_invoice": fields.Date.today(),
                "invoice_line_ids": invoice_lines1,
                "origin": "Unit test",
                "journal_id": self.journal.id,
                "account_id": self.customer.property_account_receivable_id.id,
            }
        )
        grouped_lines1 = invoice1.report_grouped_invoice_lines()
        for line in grouped_lines1:
            if line['product'] == self.product1:
                self.assertEquals(line["quantity"], 3.0)
                self.assertEquals(line["price_unit"], 100)
            if line['product'] == self.product1:
                self.assertEquals(line["quantity"], 3.0)
                self.assertEquals(line["price_unit"], 100)

    def test_group_invoice_lines_with_discount(self):
        invoice_lines2 = [
            (
                0,
                False,
                {
                    "name": self.product1.display_name,
                    "product_id": self.product1.id,
                    "quantity": 3,
                    "uom_id": self.product1.uom_id.id,
                    "discount": "10.0",
                    "price_unit": 100,
                    "account_id": self.customer.property_account_receivable_id.id,
                },
            ),
            (
                0,
                False,
                {
                    "name": self.product1.display_name,
                    "product_id": self.product1.id,
                    "quantity": 4,
                    "uom_id": self.product1.uom_id.id,
                    "discount": "10.0",
                    "price_unit": 100,
                    "account_id": self.customer.property_account_receivable_id.id,
                },
            ),
            (
                0,
                False,
                {
                    "name": self.product1.display_name,
                    "product_id": self.product1.id,
                    "quantity": 3,
                    "uom_id": self.product1.uom_id.id,
                    "discount": "0",
                    "price_unit": 100,
                    "account_id": self.customer.property_account_receivable_id.id,
                },
            ),
        ]
        invoice2 = self.env["account.invoice"].create(
            {
                "partner_id": self.customer.id,
                "type": "out_invoice",
                "date_invoice": fields.Date.today(),
                "invoice_line_ids": invoice_lines2,
                "origin": "Unit test",
                "journal_id": self.journal.id,
                "account_id": self.customer.property_account_receivable_id.id,
            }
        )
        grouped_lines2 = invoice2.report_grouped_invoice_lines()
        for line in grouped_lines2:
            if line['price_unit'] == 90.0:
                self.assertEquals(line["quantity"], 7.0)
            else:
                self.assertEquals(line["quantity"], 3.0)
                self.assertEquals(line["price_unit"], 100)
