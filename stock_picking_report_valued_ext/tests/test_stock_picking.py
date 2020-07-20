# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestStockPicking(common.TransactionCase):
    def setUp(self):
        super().setUp()
        delivery_product = self.env.ref("delivery.product_product_delivery_normal")
        test_product = self.env.ref("product.product_product_25")
        tax = self.env["account.tax"].create(
            {
                "name": "TAX 15%",
                "amount_type": "percent",
                "type_tax_use": "sale",
                "amount": 15.0,
            }
        )
        self.sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.env.ref("base.res_partner_4").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": "Delivery Charge",
                            "product_id": delivery_product.id,
                            "product_uom_qty": 1,
                            "product_uom": delivery_product.uom_po_id.id,
                            "price_unit": 100,
                            "is_delivery": True,
                            "tax_id": [(4, tax.id)],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": test_product.name,
                            "product_id": test_product.id,
                            "product_uom_qty": 1,
                            "product_uom": test_product.uom_po_id.id,
                            "price_unit": 200,
                            "is_delivery": False,
                            "tax_id": [(4, tax.id)],
                        },
                    ),
                ],
            }
        )
        self.sale_order.action_confirm()

    def test_01_delivery_price(self):
        """This Method evaluate the delivery price from sale order lines"""
        delivery_price = self.sale_order.picking_ids[0].delivery_price
        self.assertEqual(delivery_price, 115)

    def test_02_amount_total(self):
        """This Method evaluate the delivery price should be added in amount total"""
        self.sale_order.picking_ids.action_done()
        amount_total = self.sale_order.picking_ids[0].amount_total
        self.assertEqual(amount_total, 345)
