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
                "name": "Test Packing DM",
                "packing_coefficient": 211.000,
                "is_for_liquid": True,
                "box_length": 385.00,
                "box_height": 335.00,
                "box_width": 275.00,
            }
        )
        self.packing_box_id1 = self.packing_box.create(
            {
                "name": "Test Packing DSS",
                "packing_coefficient": 57.800,
                "is_for_liquid": True,
                "box_length": 300.00,
                "box_height": 210.00,
                "box_width": 160.00,
            }
        )
        self.packing_box_id2 = self.packing_box.create(
            {
                "name": "Test Packing DXL",
                "packing_coefficient": 594.530,
                "box_length": 640.00,
                "box_height": 335.00,
                "box_width": 445.00,
            }
        )
        self.packing_box_id3 = self.packing_box.create(
            {
                "name": "Test Packing LXL",
                "packing_coefficient": 362.235,
                "is_for_liquid": True,
                "box_dest_id": self.packing_box_id2.id,
                "box_length": 560.00,
                "box_height": 325.00,
                "box_width": 425.00,
            }
        )
        self.packing_box_id4 = self.packing_box.create(
            {
                "name": "Test Packing DSS",
                "packing_coefficient": 57.800,
                "box_length": 300.00,
                "box_height": 160.00,
                "box_width": 210.00,
            }
        )
        self.productA = self.env["product.product"].create(
            {
                "name": "Vitrification Kit 101",
                "type": "product",
                "has_liquid": True,
                "packing_coefficient": 3.650,
            }
        )
        self.productB = self.env["product.product"].create(
            {
                "name": "Vitrification Solution Set 110",
                "type": "product",
                "has_liquid": True,
                "packing_coefficient": 1.700,
            }
        )
        self.productC = self.env["product.product"].create(
            {
                "name": "Warming Kit 102",
                "type": "product",
                "has_liquid": True,
                "packing_coefficient": 2.120,
            }
        )
        self.productD = self.env["product.product"].create(
            {
                "name": "Warming Solution Set 205",
                "type": "product",
                "has_liquid": True,
                "packing_coefficient": 1.800,
            }
        )
        self.productE = self.env["product.product"].create(
            {
                "name": "Cooling rack",
                "type": "product",
                "min_box_id": self.packing_box_id4.id,
                "packing_coefficient": 24.800,
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
                "product_uom_qty": 9,
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
                "product_uom_qty": 6,
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
                "product_uom_qty": 10,
                "product_uom": self.productC.uom_id.id,
                "picking_id": self.picking_ship.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.move4 = self.MoveObj.create(
            {
                "name": self.productD.name,
                "product_id": self.productD.id,
                "product_uom_qty": 6,
                "product_uom": self.productD.uom_id.id,
                "picking_id": self.picking_ship.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
            }
        )
        self.move5 = self.MoveObj.create(
            {
                "name": self.productE.name,
                "product_id": self.productE.id,
                "product_uom_qty": 1,
                "product_uom": self.productE.uom_id.id,
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
        self.move5.write({"picking_id": self.picking_ship.id})
        min_box = self.picking_ship._get_min_box(self.picking_ship.move_lines)
        self.assertEqual(
            (
                self.packing_box_id0
                + self.packing_box_id1
                + self.packing_box_id2
                + self.packing_box_id3
                + self.packing_box_id4
            ).sorted(reverse=True)[0],
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
        self.assertTrue(
            self.packing_box_id3,
            self.picking_ship._get_packing_boxes(self.productD.has_liquid),
        )
        self.assertTrue(
            self.packing_box_id4,
            self.picking_ship._get_packing_boxes(self.productE.has_liquid),
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

        # CASE 1
        self.assertEqual(
            self.picking_ship.box_line_ids[0].packing_box_id,
            self.packing_box_id0,
            "Packing Box is not correctly picked up",
        )

        self.assertEqual(
            sum(box.box_quantity for box in self.picking_ship.box_line_ids),
            1,
            "please check the No. of Boxes",
        )

        self.picking_ship.write(
            {
                "move_lines": [
                    (
                        3,
                        self.picking_ship.move_lines.filtered(
                            lambda p: p.product_id.id == self.productB.id
                        ).id,
                    )
                ]
            }
        )
        self.picking_ship.write(
            {
                "move_lines": [
                    (
                        3,
                        self.picking_ship.move_lines.filtered(
                            lambda p: p.product_id.id == self.productD.id
                        ).id,
                    )
                ]
            }
        )
        self.picking_ship.move_lines[0].write({"product_uom_qty": 1})
        self.picking_ship.move_lines[1].write({"product_uom_qty": 1})

        # CASE 2
        self.assertEqual(
            sum(box.box_quantity for box in self.picking_ship.box_line_ids),
            1,
            "please check the No. of Boxes",
        )
        self.assertEqual(
            self.picking_ship.box_line_ids[0].packing_box_id,
            self.packing_box_id1,
            "please check the No. of Boxes",
        )
        self.move2.write({"product_uom_qty": 750})
        self.picking_ship.write({"move_lines": [(6, 0, [self.move2.id])]})

        # CASE 3
        self.assertEqual(
            sum(box.box_quantity for box in self.picking_ship.box_line_ids),
            4,
            "please check the No. of Boxes",
        )
        self.assertEqual(
            self.picking_ship.box_line_ids[0].packing_box_id,
            self.packing_box_id2,
            "please check the No. of Boxes",
        )
        self.assertEqual(
            self.picking_ship.box_line_ids[1].packing_box_id,
            self.packing_box_id0,
            "please check the No. of Boxes",
        )

        self.move2.write({"product_uom_qty": 1})
        self.picking_ship.write({"move_lines": [(6, 0, [self.move4.id])]})

        # CASE 4
        self.assertEqual(
            sum(box.box_quantity for box in self.picking_ship.box_line_ids),
            1,
            "please check the No. of Boxes",
        )

        self.picking_ship.write({"move_lines": [(6, 0, [self.move5.id])]})

        self.assertEqual(
            self.picking_ship.box_line_ids.packing_box_id,
            self.packing_box_id4,
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
