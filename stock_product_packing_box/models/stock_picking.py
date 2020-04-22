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
    total_packing_coefficient = fields.Float(
        string="Total Packing Coefficient",
        compute="_compute_total_packing_coefficient",
        store=True,
    )

    @api.multi
    @api.depends("move_lines")
    def _compute_total_packing_coefficient(self):
        for picking in self:
            picking.total_packing_coefficient = sum(
                picking.mapped("move_lines")
                .mapped("product_id")
                .mapped("packing_coefficient")
            )

    @api.multi
    @api.depends("total_packing_coefficient")
    def _compute_product_packing_line_ids(self):
        for picking in self:
            picking.product_packing_line_ids.unlink()
            packing_division = (
                picking.mapped("move_lines")
                .mapped("product_id")
                .mapped("product_packing_divison_id")
            )
            # Get the list of boxes in the same division
            product_packing_box_list = self.env["product.packing.box"].search(
                [
                    (
                        "product_packing_divison_id",
                        "=",
                        packing_division[0].id if packing_division else False,
                    )
                ],
                order="packing_coefficient asc",
            )
            # Find the box has the smallest packing_coefficient that fits the
            # remaining_coefficient. Use the largest box if not find, loop
            # until the remaining coefficient smaller than 0.
            remaining_coefficient = picking.total_packing_coefficient
            box_vals = {}
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
