# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _get_lots_for_scrap(self):
        self.ensure_one()
        res = self.env["stock.production.lot"].browse()
        if self.state == "done":
            res = self.finished_move_line_ids.mapped("lot_id")
        elif self.state != "cancel":
            res = self.move_raw_ids.mapped("move_line_ids").mapped("lot_id")
        return res

    @api.multi
    def button_scrap(self):
        self.ensure_one()
        res = super().button_scrap()
        lots_for_scrap = self._get_lots_for_scrap()
        res["context"].update({"lot_ids": lots_for_scrap.ids})
        return res
