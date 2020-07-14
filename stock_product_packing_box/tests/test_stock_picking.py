# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestPacking(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        customer_location = cls.env.ref("stock.stock_location_customers")

        def _create_box(name, coefficient, is_for_liquid, box_dest=None):
            return cls.env["product.packing.box"].create(
                {
                    "name": name,
                    "packing_coefficient": coefficient,
                    "is_for_liquid": is_for_liquid,
                    "box_dest_id": box_dest and box_dest.id,
                }
            )

        cls.box_d60 = _create_box("d60", 60.0, False)
        cls.box_d200 = _create_box("d200", 200.0, False)
        cls.box_d600 = _create_box("d600", 600.0, False)
        cls.box_l360 = _create_box("l360", 360.0, True, cls.box_d600)

        def _create_product(name, coefficient, has_liquid, min_box=None):
            return cls.env["product.product"].create(
                {
                    "name": name,
                    "type": "product",
                    "packing_coefficient": coefficient,
                    "has_liquid": has_liquid,
                    "min_box_id": min_box and min_box.id,
                }
            )

        cls.product1 = _create_product("test1", 1.0, False)
        cls.product2 = _create_product("test2", 4.0, True)
        cls.product3 = _create_product("test3", 25.0, False, cls.box_d200)

        cls.picking = cls.env["stock.picking"].create(
            {
                "location_id": cls.stock_location.id,
                "location_dest_id": customer_location.id,
                "picking_type_id": cls.env["ir.model.data"].xmlid_to_res_id(
                    "stock.picking_type_out"
                ),
                "box_calc_type": "initial_qty",
            }
        )

        def _create_move(product):
            return cls.env["stock.move"].create(
                {
                    "name": product.name,
                    "product_id": product.id,
                    "product_uom": product.uom_id.id,
                    "location_id": cls.stock_location.id,
                    "location_dest_id": customer_location.id,
                }
            )

        cls.move1 = _create_move(cls.product1)
        cls.move2 = _create_move(cls.product2)
        cls.move3 = _create_move(cls.product3)

    def test_01_get_moves_for_box_calc(self):
        # When box calculation is for initial qty.
        # All move lines are considered.
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        self.assertEqual(
            self.picking._get_moves_for_box_calc(), self.picking.move_lines
        )
        # When box calculation is for reserved qty.
        # No move lines are considered (since there is no reserved qty as of now).
        self.picking.write({"box_calc_type": "reserved_qty"})
        self.assertFalse(self.picking._get_moves_for_box_calc())

    def test_02_get_min_box(self):
        # With just a move line with a product with no min box setting.
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        min_box = self.picking._get_min_box(self.picking.move_lines)
        self.assertFalse(min_box)
        # With a move line with a product with min box setting.
        self.move3.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        min_box = self.picking._get_min_box(self.picking.move_lines)
        self.assertEqual(min_box, self.box_d200)

    def test_03_get_packing_boxes(self):
        # has_liquid == True
        self.assertEqual(self.picking._get_packing_boxes(True), self.box_l360)
        # has_liquid == False
        self.assertEqual(
            self.picking._get_packing_boxes(False),
            self.box_d60 + self.box_d200 + self.box_d600,
        )

    def test_04_compute_box_line_ids(self):
        # As of now, self.picking is in unreserved state
        # No boxes should be proposed when calc type is "reserved_qty" and no
        # reservation is done.
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        self.picking.write({"box_calc_type": "reserved_qty"})
        self.assertFalse(self.picking.box_line_ids)

    def test_05_compute_box_line_ids(self):
        # without liquid
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        self.assertEqual(len(self.picking.box_line_ids), 1)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d60
            )
        )
        self.assertEqual(self.picking.box_line_ids.box_quantity, 1)

        # Change qty to increase the coefficient.
        # The box for liquid (box_l360) should not be proposed.
        self.move1.write({"product_uom_qty": 300})
        self.assertEqual(len(self.picking.box_line_ids), 1)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d600
            )
        )
        self.assertEqual(self.picking.box_line_ids.box_quantity, 1)

        # Further change qty to increase the coefficient.
        # Multiple boxes should be proposed.
        self.move1.write({"product_uom_qty": 650})
        self.assertEqual(len(self.picking.box_line_ids), 2)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d600
            )
        )
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d60
            )
        )
        for line in self.picking.box_line_ids:
            if line.packing_box_id == self.box_d600:
                self.assertEqual(line.box_quantity, 1)
            if line.packing_box_id == self.box_d60:
                self.assertEqual(line.box_quantity, 1)

    def test_06_compute_box_line_ids(self):
        # with liquid
        # A box should be proposed upon conversion (liquid box -> dry box).
        self.move2.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        self.assertEqual(len(self.picking.box_line_ids), 1)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d600
            )
        )
        self.assertEqual(self.picking.box_line_ids.box_quantity, 1)

    def test_07_compute_box_line_ids(self):
        # with a product with min_box setting
        # A box should be proposed upon conversion (-> min box).
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        self.move3.write({"picking_id": self.picking.id, "product_uom_qty": 1})
        self.assertEqual(len(self.picking.box_line_ids), 1)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d200
            )
        )
        self.assertEqual(self.picking.box_line_ids.box_quantity, 1)

    def test_08_recompute_product_packing(self):
        # Recompute after box definitions is updated.
        # A box should be proposed using the latest box definition.
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 1000})
        self.box_d200.write({"packing_coefficient": 1000})
        self.picking.recompute_product_packing()
        self.assertEqual(len(self.picking.box_line_ids), 1)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d200
            )
        )
        self.assertEqual(self.picking.box_line_ids.box_quantity, 1)

    def test_09_get_packing_coefficient(self):
        # Create partial stock, reserve it and calculate boxes for reserved qty.
        # A box should be proposed for reserved qty instead of initial qty.
        self.picking.write({"box_calc_type": "reserved_qty"})
        self.move1.write({"picking_id": self.picking.id, "product_uom_qty": 100})
        self.env["stock.quant"].create(
            {
                "product_id": self.product1.id,
                "location_id": self.stock_location.id,
                "quantity": 50.0,
            }
        )
        self.picking.action_assign()
        self.assertEqual(len(self.picking.box_line_ids), 1)
        self.assertTrue(
            self.picking.box_line_ids.filtered(
                lambda x: x.packing_box_id == self.box_d60
            )
        )
        self.assertEqual(self.picking.box_line_ids.box_quantity, 1)
