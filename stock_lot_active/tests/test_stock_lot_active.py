# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase, tagged


@tagged("standard", "at_install")
class TestStockLotActive(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        picking_type = cls.env["stock.picking.type"].browse(
            cls.env["ir.model.data"].xmlid_to_res_id("stock.picking_type_in")
        )
        stock_location = cls.env.ref("stock.stock_location_stock")
        supplier_location = cls.env.ref("stock.stock_location_suppliers")

        product = cls.env["product.product"].create(
            {"name": "test product", "type": "product", "tracking": "lot"}
        )
        cls.lot = cls.env["stock.production.lot"].create({"product_id": product.id})

        cls.picking = cls.env["stock.picking"].create(
            {
                "location_id": supplier_location.id,
                "location_dest_id": stock_location.id,
                "picking_type_id": picking_type.id,
            }
        )
        cls.move = cls.env["stock.move"].create(
            {
                "name": product.name,
                "product_id": product.id,
                "product_uom": product.uom_id.id,
                "product_uom_qty": 1.0,
                "location_id": supplier_location.id,
                "location_dest_id": stock_location.id,
                "picking_id": cls.picking.id,
            }
        )

    def test_01_archive_lot(self):
        # There should be no constraint error when there is no associated quants.
        self.lot.active = False

        self.lot.active = True

        self.picking.action_confirm()
        self.picking.action_assign()
        self.picking.move_line_ids[0].lot_id = self.lot
        self.picking.move_line_ids[0].qty_done = 1.0
        self.picking.button_validate()
        self.assertEqual(len(self.lot.quant_ids), 2)
        # Error should be raised when there is a quant linked to the lot.
        with self.assertRaises(ValidationError):
            self.lot.active = False
