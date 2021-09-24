# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestStockLotActive(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.lot_obj = cls.env["stock.production.lot"].sudo(cls.user_demo)
        picking_type = cls.env["stock.picking.type"].browse(
            cls.env["ir.model.data"].xmlid_to_res_id("stock.picking_type_in")
        )
        stock_location = cls.env.ref("stock.stock_location_stock")
        supplier_location = cls.env.ref("stock.stock_location_suppliers")
        product = cls.env["product.product"]

        def _create_product(name, lot_type=False):
            return product.create(
                {
                    "name": name,
                    "type": "product",
                    "tracking": "lot",
                    # "lot_type": lot_type,
                }
            )

        cls.prod_sol = _create_product("Solution", "sol")

        cls.picking = cls.env["stock.picking"].create(
            {
                "location_id": supplier_location.id,
                "location_dest_id": stock_location.id,
                "picking_type_id": picking_type.id,
            }
        )

        def _create_move(product):
            return cls.env["stock.move"].create(
                {
                    "name": product.name,
                    "product_id": product.id,
                    "product_uom": product.uom_id.id,
                    "product_uom_qty": 10.0,
                    "location_id": supplier_location.id,
                    "location_dest_id": stock_location.id,
                    "picking_id": cls.picking.id,
                }
            )

        cls.move1 = _create_move(cls.prod_placeholder)

    def test_01_receive_sol(self):
        self.move1.product_id = self.prod_sol
        self.picking.action_confirm()
        self.picking.action_assign()
        lot = self.lot_obj.create({"product_id": self.move1.product_id.id})
        self.picking.move_line_ids[0].lot_id = lot
        self.picking.button_validate()
        lot.date_received = fields.Date.from_string("2020-12-09")
        self.assertEqual(lot.ref, "VS1209AA")
