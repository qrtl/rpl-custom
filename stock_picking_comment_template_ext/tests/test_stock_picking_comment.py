# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.sale.tests.test_sale_order import TestSaleOrder


@tagged("-at_install", "post_install")
class TestStockPickingComment(TestSaleOrder):
    def test_00_stock_picking_comment(self):
        """ Confirm that sales order staff memo (note2) is reflected on
            related pickings.
        """
        self.sale_order.write({"note2": "test comment"})
        self.sale_order.action_confirm()
        for picking in self.sale_order.picking_ids:
            self.assertEqual(self.sale_order.note2, picking.note2)
