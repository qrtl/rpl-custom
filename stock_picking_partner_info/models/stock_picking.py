# Copyright 2021 Quartile Limited

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    phone = fields.Char(related="partner_id.phone")
