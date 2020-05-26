# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    box_line_ids = fields.One2many(
        "product.packing.line",
        "picking_id",
        string="Packing Boxes",
        compute="_compute_box_line_ids",
        store=True,
    )
    box_calc_type = fields.Selection(
        [
            ("initial_qty", "Initial Demand Quantity"),
            ("reserved_qty", "Reserved Quantity"),
        ],
        string="Calculation Type",
        default="initial_qty",
    )

    def _get_moves_for_box_calc(self):
        self.ensure_one()
        res = self.env["stock.move"].browse()
        if self.box_calc_type == "initial_qty":
            res = self.move_lines
        else:  # box_calc_type == "reserved_qty"
            res = self.move_lines.filtered(lambda x: x.reserved_availability > 0)
        return res

    def _get_min_box(self, moves):
        self.ensure_one()
        res = False
        min_boxes = moves.mapped("product_id").mapped("min_box_id")
        if min_boxes:
            # pick the largest among "min boxes"
            res = min_boxes.sorted("packing_coefficient", reverse=True)[0]
        return res

    def _get_packing_boxes(self, has_liquid):
        self.ensure_one()
        res = self.env["product.packing.box"].search(
            [("is_for_liquid", "=", has_liquid)], order="packing_coefficient asc",
        )
        return res

    @api.multi
    @api.depends("move_lines.product_uom_qty", "move_lines.reserved_availability")
    def _compute_box_line_ids(self):
        for picking in self:
            picking.box_line_ids.unlink()
            moves = picking._get_moves_for_box_calc()
            min_box = picking._get_min_box(moves)
            has_liquid = any(move.product_id.has_liquid for move in moves)
            packing_boxes = picking._get_packing_boxes(has_liquid)
            coefficient_bal = moves._get_packing_coefficient()
            box_vals = {}
            # Find the box that has the smallest packing_coefficient that fits
            # coefficient_bal. Use the largest box if not found, and loop
            # until remaining coefficient is not larger than 0.
            if packing_boxes:
                while coefficient_bal > 0.0:
                    box = False
                    for packing_box in packing_boxes:
                        if packing_box.packing_coefficient >= coefficient_bal:
                            box = packing_box
                            break
                    box = box or packing_boxes[-1]
                    coefficient_bal -= box.packing_coefficient
                    box = box._convert_packing_box(min_box)
                    if box.id not in box_vals:
                        box_vals[box.id] = 1
                    else:
                        box_vals[box.id] += 1
                picking.box_line_ids = [
                    (0, 0, {"packing_box_id": box, "box_quantity": number})
                    for box, number in box_vals.items()
                ]

    def recompute_product_packing(self):
        self._compute_box_line_ids()
