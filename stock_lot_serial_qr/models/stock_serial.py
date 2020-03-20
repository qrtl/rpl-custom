# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockSerial(models.Model):
    _name = "stock.serial"
    _description = "Stock Serial Numbers"

    name = fields.Char(string="Name", readonly=True,)
    lot_id = fields.Many2one("stock.production.lot", string="Lot", readonly=False,)
    product_id = fields.Many2one(
        related="lot_id.product_id", string="Product", store=True,
    )
    quantity = fields.Float(string="Quantity", required=True, readonly=False,)
    qr_code_image = fields.Binary(string="QR Code", readonly=True,)
    attachment_id = fields.Many2one(
        "ir.attachment", string="Attachment", readonly=False,
    )

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code("stock.serial")
        return super(StockSerial, self).create(vals)
