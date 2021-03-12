# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    increase_refrigerant = fields.Boolean("Increase Refrigerant",)