# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    product_packing_line_ids = fields.One2many(
        "product.packing.line",
        "picking_id",
        string="Packing Box(es)",
        compute="_compute_product_packing_line_ids",
        store=True,
    )

    @api.multi
    @api.depends("move_lines")
    def _compute_product_packing_line_ids(self):
        for picking in self:
            picking.product_packing_line_ids.unlink()
            packing_divisions = (
                picking.mapped("move_lines")
                .mapped("product_id")
                .mapped("product_packing_divison_id")
            )   
            box_vals = {}
            for division in packing_divisions:
                # Get the list of boxes in the same division
                product_packing_box_list = self.env["product.packing.box"].search(
                    [
                        (
                            "product_packing_divison_id",
                            "=",
                            division.id,
                        ),
                        (
                            "exception_product_ids", "not in", picking.mapped("move_lines").mapped("product_id").ids
                        )
                    ],
                    order="packing_coefficient asc",
                )
                # Find the box has the smallest packing_coefficient that fits the
                # remaining_coefficient. Use the largest box if not find, loop
                # until the remaining coefficient smaller than 0.
                remaining_coefficient = sum(picking.mapped("move_lines").mapped("product_id").filtered(lambda x: x.product_packing_divison_id == division).mapped("packing_coefficient"))
                while remaining_coefficient > 0:
                    fit_box = (
                        product_packing_box_list.filtered(
                            lambda x: x.packing_coefficient >= remaining_coefficient
                        )[0]
                        if product_packing_box_list.filtered(
                            lambda x: x.packing_coefficient >= remaining_coefficient
                        )
                        else product_packing_box_list[-1]
                    )
                    remaining_coefficient = (
                        remaining_coefficient - fit_box.packing_coefficient
                    )
                    if fit_box.id not in box_vals:
                        box_vals[fit_box.id] = 1
                    else:
                        box_vals[fit_box.id] += 1
            # Create product.packing.line based on the box_vals
            for box, number in box_vals.items():
                self.env["product.packing.line"].create(
                    {
                        "picking_id": picking.id,
                        "product_packing_box_id": box,
                        "number_of_package": number,
                    }
                )

    def recompute_product_packing(self):
        self._compute_product_packing_line_ids()
