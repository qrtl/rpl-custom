# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    assigned_lot_ids = fields.Many2many(
        "stock.production.lot",
        compute="_compute_assigned_lot_ids",
        string="Assigned Lots",
    )

    def _compute_assigned_lot_ids(self):
        for move in self:
            if move.move_line_ids:
                move.assigned_lot_ids = move.move_line_ids.mapped("lot_id")
