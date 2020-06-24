# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestStockPicking(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner_delta_id = self.env.ref(
            'base.res_partner_4')
        product_01 = self.env['product.product'].create({
            'name': 'product 01',
            'type': 'product',
        })
        product_02 = self.env['product.product'].create({
            'name': 'product 02',
            'type': 'product',
        })
        self.sale_order_01 = self.env['sale.order'].create({
            'partner_id': self.partner_delta_id.id,
            'order_line': [
                (0, 0, {
                    'name': product_01.name,
                    'product_id': product_01.id,
                    'product_uom_qty': 1,
                    'product_uom': product_01.uom_po_id.id,
                    'price_unit': 100,
                    'is_delivery': True,
                }),
                (0, 0, {
                    'name': product_02.name,
                    'product_id': product_02.id,
                    'product_uom_qty': 1,
                    'product_uom': product_02.uom_po_id.id,
                    'price_unit': 200,
                    'is_delivery': False,
                })
            ],
        })
        self.sale_order_01.action_confirm()

    def test_compute_delivery_price(self):
        """This Method evaluate the delivery price from sale order lines"""

        delivery_price = self.sale_order_01.picking_ids[0].delivery_price
        self.assertEqual(delivery_price, 115)

    def test_compute_amount_all(self):
        """This Method evaluate the delivery price
        should be added in amount total"""

        self.sale_order_01.picking_ids[0].move_lines[0].quantity_done = 1
        amount_total = self.sale_order_01.picking_ids[0].amount_total
        self.assertEqual(amount_total, 230)
