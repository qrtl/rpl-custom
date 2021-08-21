# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_lots_for_scrap(self):
        self.ensure_one()
        return self.move_line_ids.mapped("lot_id")

    @api.multi
    def button_scrap(self):
        self.ensure_one()
        res = super().button_scrap()
        lots_for_scrap = self._get_lots_for_scrap()
        res["context"].update({"lot_ids": lots_for_scrap.ids})
        return res
