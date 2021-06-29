# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestMrpProductionProposeLocation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def _create_product(name, use_alt_location_dest=False):
            return cls.env["product.product"].create(
                {
                    "name": name,
                    "type": "product",
                    "use_alt_location_dest": use_alt_location_dest
                }
            )

        cls.prod_fp01 = _create_product("fp01")
        cls.prod_fp02 = _create_product("fp02", use_alt_location_dest=True)
        cls.prod_rm = _create_product("rm")

        def _create_bom(parent, component, qty):
            return cls.env["mrp.bom"].create(
                {
                    "product_id": parent.id,
                    "product_tmpl_id": parent.product_tmpl_id.id,
                    "product_uom_id": parent.uom_id.id,
                    "product_qty": 1.0,
                    "type": "normal",
                    "bom_line_ids": [
                        (0, 0, {"product_id": component.id, "product_qty": qty}),
                    ],
                }
            )

        cls.bom_fp01 = _create_bom(cls.prod_fp01, cls.prod_rm, 1.0)
        cls.bom_fp02 = _create_bom(cls.prod_fp02, cls.prod_rm, 1.0)

        cls.pick_type = cls.env["stock.picking.type"].search([("code", "=", "mrp_operation")])[:1]
        cls.default_location_dest = cls.pick_type.default_location_dest_id
        cls.alt_location_dest = cls.env["stock.location"].create({"name": "alt location dest", "location_id": cls.default_location_dest.location_id.id})

    def test_01_onchange_picking_type(self):
        mo = self.env["mrp.production"].create(
            {
                "picking_type_id": self.pick_type.id,
                "product_id": self.prod_fp01.id,
                "product_uom_id": self.prod_fp01.uom_id.id,
                "product_qty": 1.0,
                "bom_id": self.bom_fp01.id,
            }
        )
        mo.onchange_picking_type()
        self.assertEqual(mo.location_dest_id, self.default_location_dest)
        self.pick_type.write({"alt_location_dest_id": self.alt_location_dest.id})
        mo.onchange_picking_type()
        self.assertEqual(mo.location_dest_id, self.default_location_dest)

    def test_02_onchange_picking_type(self):
        mo = self.env["mrp.production"].create(
            {
                "picking_type_id": self.pick_type.id,
                "product_id": self.prod_fp02.id,
                "product_uom_id": self.prod_fp02.uom_id.id,
                "product_qty": 1.0,
                "bom_id": self.bom_fp02.id,
            }
        )
        mo.onchange_picking_type()
        self.assertEqual(mo.location_dest_id, self.default_location_dest)
        self.pick_type.write({"alt_location_dest_id": self.alt_location_dest.id})
        mo.onchange_picking_type()
        # Alt. location dest is proposed only for this case - picking type has
        # the alt. location dest set, and the product indicates to use it.
        self.assertEqual(mo.location_dest_id, self.alt_location_dest)
