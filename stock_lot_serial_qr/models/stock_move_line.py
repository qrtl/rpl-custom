# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    # this will check if new lot will appear on incoming shipment
    # then it will create serial numbers for newly created lot
    @api.multi
    def write(self, vals):
        result = super(StockMoveLine, self).write(vals)
        if 'lot_id' in vals:
            for move_line in self.filtered(
                lambda x: x.picking_id.picking_type_code == 'incoming'):
                if move_line.qty_done and move_line.lot_id:
                    move_line.lot_id._create_stock_serial(move_line.qty_done)
        return result
