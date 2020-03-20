# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    lot_line_ids = fields.One2many(
        "stock.serial", "lot_id", required=True, readonly=True
    )

    @api.multi
    def _create_stock_serial(self, quantity):
        for lot in self:
            for _i in range(int(quantity)):
                vals = {
                    "quantity": 1,
                    "lot_id": lot.id,
                }
                serial_id = self.env["stock.serial"].create(vals)
                barcode = self.env["ir.actions.report"].barcode(
                    "QR",
                    value=serial_id.name,
                    width=200,
                    height=200,
                    humanreadable=True,
                )
                attachment_vals = {
                    "res_name": serial_id.name,
                    "res_model": "stock.serial",
                    "res_id": serial_id.id,
                    "datas": base64.encodestring(barcode),
                    "type": "binary",
                    "datas_fname": serial_id.name + ".png",
                    "name": serial_id.name,
                }
                attachment_id = self.env["ir.attachment"].create(attachment_vals)
                serial_id.update(
                    {
                        "attachment_id": attachment_id.id,
                        "qr_code_image": base64.encodestring(barcode),
                    }
                )

    @api.multi
    def action_serial_number(self):
        self.ensure_one()
        action = self.env.ref("stock_lot_serial_qr.action_stock_serial")
        action_read = action.read([])[0]
        action_read["domain"] = [("lot_id", "=", self.id)]
        return action_read
