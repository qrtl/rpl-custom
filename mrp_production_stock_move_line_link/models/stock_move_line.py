# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    qty_to_reserve = fields.Float(
        "Real Quantity to Reserve",
        digits=0,
        compute="_compute_qty_to_reserve",
        store=True,
        readonly=True,
    )
    uom_qty_to_reserve = fields.Float(
        "Quantity to Reserve",
        default=0.0,
        digits=dp.get_precision("Product Unit of Measure"),
    )

    @api.one
    @api.depends("product_id", "product_uom_id", "uom_qty_to_reserve")
    def _compute_qty_to_reserve(self):
        self.qty_to_reserve = self.product_uom_id._compute_quantity(
            self.uom_qty_to_reserve, self.product_id.uom_id, rounding_method="HALF-UP"
        )

    # def write(self, vals):
    #     res = super().write(vals)
    #     if not self.env.context.get("bypass_reservation_update"):
    #         moves = self.mapped("move_id")
    #         for move in moves.with_context(bypass_reservation_update=True):
    #             move._action_assign()
    #     return res
