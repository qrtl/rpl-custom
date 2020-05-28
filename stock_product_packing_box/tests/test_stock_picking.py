# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestPacking(TransactionCase):
    def setUp(self):
        super(TestPacking, self).setUp()
        self.ModelDataObj = self.env["ir.model.data"]
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.warehouse = self.env["stock.warehouse"].search([], limit=1)
        self.warehouse.write({"delivery_steps": "pick_pack_ship"})
        self.ship_location = self.warehouse.wh_output_stock_loc_id
        self.customer_location = self.env.ref("stock.stock_location_customers")
        self.partner_delta_id = self.ModelDataObj.xmlid_to_res_id("base.res_partner_4")
        self.picking_type_out = self.ModelDataObj.xmlid_to_res_id(
            "stock.picking_type_out"
        )
        self.MoveObj = self.env["stock.move"]

        self.packing_box = self.env["product.packing.box"]

        self.packing_box_id0 = self.packing_box.create(
            {
                "name": "Test Packing Box 1",
                "packing_coefficient": 0.25,
                "box_length": 10,
                "box_height": 20,
                "box_width": 30,
            }
        )
        self.packing_box_id1 = self.packing_box.create(
            {
                "name": "Test Packing Box 2",
                "packing_coefficient": 0.50,
                "box_length": 20,
                "box_height": 40,
                "box_width": 60,
            }
        )
        self.packing_box_id2 = self.packing_box.create(
            {
                "name": "Test Packing Box 3",
                "packing_coefficient": 0.75,
                "is_for_liquid": True,
                "box_length": 30,
                "box_height": 60,
                "box_width": 90,
            }
        )
        self.productA = self.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
                "has_liquid": False,
                "min_box_id": self.packing_box_id0.id,
                "packing_coefficient": 0.15,
            }
        )
        self.productB = self.env["product.product"].create(
            {
                "name": "Product B",
                "type": "product",
                "has_liquid": False,
                "min_box_id": self.packing_box_id1.id,
                "packing_coefficient": 0.25,
            }
        )
        self.productC = self.env["product.product"].create(
            {
                "name": "Product C",
                "type": "product",
                "has_liquid": True,
                "min_box_id": self.packing_box_id2.id,
                "packing_coefficient": 0.35,
            }
        )

        self.picking_ship = self.env["stock.picking"].create(
            {
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "partner_id": self.partner_delta_id,
                "picking_type_id": self.picking_type_out,
            }
        )
        self.move1 = self.MoveObj.create(
            {
                "name": self.productA.name,
                "product_id": self.productA.id,
                "product_uom_qty": 200,
                "product_uom": self.productA.uom_id.id,
                "picking_id": self.picking_ship.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.move2 = self.MoveObj.create(
            {
                "name": self.productB.name,
                "product_id": self.productB.id,
                "product_uom_qty": 300,
                "product_uom": self.productB.uom_id.id,
                "picking_id": self.picking_ship.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.move3 = self.MoveObj.create(
            {
                "name": self.productC.name,
                "product_id": self.productC.id,
                "product_uom_qty": 300,
                "product_uom": self.productC.uom_id.id,
                "picking_id": self.picking_ship.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )

    def test_01_get_moves_for_box_calc(self):
        self.picking_ship.action_assign()
        self.assertEqual(
            self.picking_ship._get_moves_for_box_calc(), self.picking_ship.move_lines
        )
        self.picking_ship.write({"box_calc_type": "reserved_qty"})
        self.picking_ship.do_unreserve()
        self.assertFalse(self.picking_ship._get_moves_for_box_calc())

    def test_02_get_min_box(self):
        min_box = self.picking_ship._get_min_box(self.picking_ship.move_lines)
        self.assertEqual(
            (self.packing_box_id0 + self.packing_box_id1 + self.packing_box_id2).sorted(
                reverse=True
            )[0],
            min_box,
        )

    def test_03_get_packing_boxes(self):
        self.assertTrue(
            self.packing_box_id0,
            self.picking_ship._get_packing_boxes(self.productA.has_liquid),
        )
        self.assertTrue(
            self.packing_box_id1,
            self.picking_ship._get_packing_boxes(self.productB.has_liquid),
        )
        self.assertTrue(
            self.packing_box_id2,
            self.picking_ship._get_packing_boxes(self.productC.has_liquid),
        )

    def test_04_compute_box_line_ids(self):
        self.picking_ship.do_unreserve()
        self.picking_ship.write({"box_calc_type": "reserved_qty"})
        self.picking_ship.recompute_product_packing()
        self.assertFalse(
            self.picking_ship.box_line_ids,
            "Box should not be add while picking "
            "is unreserved and box calc type is reserved.",
        )

        self.picking_ship.action_assign()
        self.picking_ship.write({"box_calc_type": "initial_qty"})
        self.picking_ship.recompute_product_packing()
        self.assertEqual(
            self.picking_ship.box_line_ids[0].packing_box_id,
            self.packing_box_id2,
            "Packing Box is not correctly picked up",
        )
        self.assertEqual(
            self.picking_ship.box_line_ids[0].box_quantity,
            280,
            "please check the No. of Boxes",
        )
        self.picking_ship.write(
            {"move_lines": [(3, self.picking_ship.move_lines[2].id)]}
        )
        self.assertEqual(
            self.picking_ship.box_line_ids[0].box_quantity,
            210,
            "please check the No. of Boxes",
        )

        self.picking_ship.write(
            {"move_lines": [(3, self.picking_ship.move_lines[1].id)]}
        )
        self.assertEqual(
            self.picking_ship.box_line_ids[0].box_quantity,
            15,
            "please check the No. of Boxes",
        )

    def test_05_recompute_product_packing(self):
        self.picking_ship.recompute_product_packing()
        self.assertTrue(self.picking_ship.box_line_ids, "Box Should be Calculated")

    def test_06_get_packing_coefficient(self):
        self.picking_ship.action_assign()

        packing_coefficient = (
            self.move1.product_uom_qty * self.productA.packing_coefficient
        )
        self.assertEqual(self.move1._get_packing_coefficient(), packing_coefficient)

        packing_coefficient = (
            self.move2.product_uom_qty * self.productB.packing_coefficient
        )
        self.assertEqual(self.move2._get_packing_coefficient(), packing_coefficient)

        packing_coefficient = (
            self.move3.product_uom_qty * self.productC.packing_coefficient
        )
        self.assertEqual(self.move3._get_packing_coefficient(), packing_coefficient)

    def test_07_convert_packing_box(self):
        self.packing_box_id0.write({"box_dest_id": self.packing_box_id1.id})
        self.assertEqual(
            self.packing_box_id0._convert_packing_box(self.packing_box_id2),
            self.packing_box_id2,
        )
