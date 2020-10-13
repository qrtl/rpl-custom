# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.addons.mrp_subcontracting.tests.common import TestMrpSubcontractingCommon

from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestMrpSubcontractingPurchaseOrder(TestMrpSubcontractingCommon):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
    
    def _create_sub_po(cls, products):
        po = cls.env["purchase.order"].create({
            'partner_id': cls.subcontractor_partner1.id,
            'order_line': [(0, 0, {
                'name': product.name,
                'product_id': product.id,
                'product_qty': 5.0,
                'product_uom': product.uom_id.id,
                'price_unit': 10,
                'date_planned': fields.Datetime.now()
            }) for product in products]
        })
        po.button_confirm()
        return po

    def test_01_prepare_subcontract_mo_vals(self):
        purchase_order = self._create_sub_po(self.finished)
        for picking in purchase_order.picking_ids:
            for move in picking.move_lines:
                self.assertEqual(picking._prepare_subcontract_mo_vals(move, move._get_subcontract_bom())['purchase_order_id'], purchase_order.id)

    def test_02_compute_subcontract_production_count(self):
        purchase_order1 = self._create_sub_po(self.finished)
        purchase_order2 = self._create_sub_po(self.finished + self.finished)
        self.assertEqual(purchase_order1.subcontract_production_count, 1)
        self.assertEqual(purchase_order2.subcontract_production_count, 2)
