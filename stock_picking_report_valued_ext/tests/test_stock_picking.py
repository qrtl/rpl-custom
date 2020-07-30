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
                            "product_uom_qty": 2,
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
        self.sale_order.picking_ids.mapped('move_line_ids').update({
            'qty_done': 1
        })
        backorder_wizard_dict = self.sale_order.picking_ids.button_validate()
        backorder_wizard = self.env[backorder_wizard_dict['res_model']].browse(backorder_wizard_dict['res_id'])
        backorder_wizard.process()

    def test_01_delivery_price(self):
        """This Method evaluate the delivery price from sale order lines"""
        for picking in self.sale_order.picking_ids:
            if not picking.backorder_id:
                self.assertEqual(picking.delivery_price, 115)
            else:
                self.assertEqual(picking.delivery_price, 0)

    def test_02_amount_total(self):
        """This Method evaluate the delivery price should be added in amount total"""
        for picking in self.sale_order.picking_ids:
            if not picking.backorder_id:
                self.assertEqual(picking.amount_total, 345)
            else:
                self.assertEqual(picking.amount_total, 230)
