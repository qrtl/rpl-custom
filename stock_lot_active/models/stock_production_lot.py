# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    active = fields.Boolean(default=True)
