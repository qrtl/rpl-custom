# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        note1 = self.sale_line_id.order_id.note1
        note2 = self.sale_line_id.order_id.note2
        if note1:
            vals["note1"] = note1
        if note2:
            vals["note2"] = note2
        return vals
