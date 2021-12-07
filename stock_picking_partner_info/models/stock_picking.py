# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    phone = fields.Char(related="partner_id.phone")
