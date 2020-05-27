# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    note2 = fields.Html(compute="_compute_note2",)

    @api.multi
    def _compute_note2(self):
        for picking in self:
            picking.note2 = picking.group_id.sale_id.note2
