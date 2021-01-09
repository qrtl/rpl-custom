# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_round

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
    quant_id = fields.Many2one("stock.quant", string="Quant")
    quant_available_uom_qty = fields.Float(
        compute="_compute_quant_available_uom_qty",
        string="Available Qty",
        store=True,
    )

    @api.one
    @api.depends("product_id", "product_uom_id", "uom_qty_to_reserve")
    def _compute_qty_to_reserve(self):
        self.qty_to_reserve = self.product_uom_id._compute_quantity(
            self.uom_qty_to_reserve, self.product_id.uom_id, rounding_method="HALF-UP"
        )

    @api.depends("quant_id")
    def _compute_quant_available_uom_qty(self):
        rounding = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for line in self:
            if line.quant_id:
                available_qty = line.quant_id.quantity - line.quant_id.reserved_quantity
                uom_qty = line.product_id.uom_id._compute_quantity(
                    available_qty, line.product_uom_id, rounding_method="HALF-UP"
                )
                line.quant_available_uom_qty = float_round(uom_qty, precision_digits=rounding)
