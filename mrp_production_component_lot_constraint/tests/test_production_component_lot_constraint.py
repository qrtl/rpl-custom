# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import Form
from odoo.tests import SavepointCase, tagged
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class TestComponentLotConstraint(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def _create_product(name, product_type, tracking, lot_restriction):
            return cls.env["product.product"].create(
                {
                    "name": name,
                    "type": product_type,
                    "tracking": tracking,
                    "lot_restriction": lot_restriction,
                }
            )
        cls.product_1 = _create_product("product 1", "product", "lot", False)
        cls.product_2 = _create_product("product 2", "product", "lot", True)
        cls.product_3 = _create_product("product 3", "product", "lot", True)

        cls.bom_1 = cls.env["mrp.bom"].create(
            {
                "product_id": cls.product_1.id,
                "product_tmpl_id": cls.product_1.product_tmpl_id.id,
                "product_uom_id": cls.product_1.uom_id.id,
                "product_qty": 1.0,
                "type": "normal",
                "bom_line_ids": [
                    (0, 0, {"product_id": cls.product_2.id, "product_qty": 1.0}),
                    (0, 0, {"product_id": cls.product_3.id, "product_qty": 2.0}),
                ]
            }
        )

        cls.location = cls.env.ref("stock.warehouse0").lot_stock_id
        
        def _create_lot(name, ref, product):
            return cls.env["stock.production.lot"].create(
                {
                    "name": name,
                    "ref": ref,
                    "product_id": product.id,
                }
            )
        # Here we set the same values to both name and ref fields for a
        # reason - when stock_lot_reference_rpl is installed, ref field
        # becomes a compute field.
        cls.lot_1 = _create_lot("AAAA0001aa", "AAAA0001aa", cls.product_2)
        cls.lot_2 = _create_lot("AAAA0001ab", "AAAA0001ab", cls.product_2)
        cls.lot_3 = _create_lot("AAAA0002aa", "AAAA0002aa", cls.product_2)
        cls.lot_4 = _create_lot("BBBB0001aa", "BBBB0001aa", cls.product_3)

        def _create_quant(product, lot, quantity):
            return cls.env["stock.quant"].create(
                {
                    "product_id": product.id,
                    "lot_id": lot.id,
                    "location_id": cls.location.id,
                    "quantity": quantity,
                }
            )
        cls.quant_1 = _create_quant(cls.product_2, cls.lot_1, 100.0)
        cls.quant_2 = _create_quant(cls.product_2, cls.lot_2, 100.0)
        cls.quant_3 = _create_quant(cls.product_2, cls.lot_3, 100.0)
        cls.quant_4 = _create_quant(cls.product_3, cls.lot_4, 100.0)

        cls.mo_1 = cls.env["mrp.production"].create(
            {
                "name": "test mo 1",
                "product_id": cls.product_1.id,
                "product_uom_id": cls.product_1.uom_id.id,
                "product_qty": 10,
                "bom_id": cls.bom_1.id,
            }
        )
        cls.move_1 = cls.mo_1.move_raw_ids.filtered(lambda x: x.product_id == cls.product_2)[:1]
        cls.move_2 = cls.mo_1.move_raw_ids.filtered(lambda x: x.product_id == cls.product_3)[:1]

    def test_01_component_lot_filter_quant_domain(self):
        wizard = self.env["assign.manual.quants"].with_context(
            active_id=self.move_1.id).create({})
        self.assertEqual(len(wizard.quants_lines), 3)
        self.mo_1.write({"component_lot_filter": "AAAA0001"})
        wizard = self.env["assign.manual.quants"].with_context(
            active_id=self.move_1.id).create({})
        self.assertEqual(len(wizard.quants_lines), 2)
        self.mo_1.write({"component_lot_filter": "AAAA0002"})
        wizard = self.env["assign.manual.quants"].with_context(
            active_id=self.move_1.id).create({})
        self.assertEqual(len(wizard.quants_lines), 1)

    def test_02_component_lot_filter_constraint(self):
        # UserError should be raised when there is a component with
        # lot_restriction and no filter is set.
        with self.assertRaises(UserError):
            self.mo_1.open_produce_product()

        # Create a move line with lot 'AAAA0002'.
        self.env["stock.move.line"].create({
            "move_id": self.move_1.id,
            "location_id": self.move_1.location_id.id,
            "location_dest_id": self.move_1.location_dest_id.id,
            "product_id": self.move_1.product_id.id,
            "product_uom_id": self.move_1.product_uom.id,
            "lot_id": self.lot_3.id,
        })
        self.mo_1.write({"component_lot_filter": "AAAA0001"})
        with self.assertRaises(UserError):
            self.mo_1.open_produce_product()
        self.mo_1.write({"component_lot_filter": "AAAA0002"})
        self.mo_1.open_produce_product()

    def test_03_select_multi_lots_per_move(self):
        self.mo_1.write({"component_lot_filter": "AAAA0001"})
        self.env["stock.move.line"].create({
            "move_id": self.move_1.id,
            "location_id": self.move_1.location_id.id,
            "location_dest_id": self.move_1.location_dest_id.id,
            "product_id": self.move_1.product_id.id,
            "product_uom_id": self.move_1.product_uom.id,
            "lot_id": self.lot_1.id,
        })
        self.env["stock.move.line"].create({
            "move_id": self.move_1.id,
            "location_id": self.move_1.location_id.id,
            "location_dest_id": self.move_1.location_dest_id.id,
            "product_id": self.move_1.product_id.id,
            "product_uom_id": self.move_1.product_uom.id,
            "lot_id": self.lot_2.id,
        })
        # Not allowed to use more than one lot per component line
        with self.assertRaises(UserError):
            self.mo_1.open_produce_product()

    def test_04_suggested_quantity(self):
        self.env["stock.move.line"].create({
            "move_id": self.move_1.id,
            "location_id": self.move_1.location_id.id,
            "location_dest_id": self.move_1.location_dest_id.id,
            "product_id": self.move_1.product_id.id,
            "product_uom_id": self.move_1.product_uom.id,
            "lot_id": self.lot_1.id,
        })
        self.assertEqual(self.mo_1.suggested_qty, 100.0)
        self.env["stock.move.line"].create({
            "move_id": self.move_2.id,
            "location_id": self.move_2.location_id.id,
            "location_dest_id": self.move_2.location_dest_id.id,
            "product_id": self.move_2.product_id.id,
            "product_uom_id": self.move_2.product_uom.id,
            "lot_id": self.lot_4.id,
        })
        self.assertEqual(self.mo_1.suggested_qty, 50.0)

    def test_05_production_qty_change(self):
        wizard = self.env["assign.manual.quants"].with_context(
            active_id=self.move_1.id).create({})
        quant_line = wizard.quants_lines.filtered(lambda x: x.lot_id == self.lot_1)[:1]
        quant_line.write(
            {
                "selected": True,
                "qty": 10
            }
        )
        wizard.assign_quants()
        # Change MO quantity from 10 to 20.
        update_quantity_wizard = self.env['change.production.qty'].create({
            'mo_id': self.mo_1.id,
            'product_qty': 20.0,
        })
        update_quantity_wizard.change_prod_qty()
        move_line = self.move_1.move_line_ids[:1]
        self.assertEqual(move_line.product_qty, 20.0)
