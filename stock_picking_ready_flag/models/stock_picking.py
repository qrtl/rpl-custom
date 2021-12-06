# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_ready = fields.Boolean(default=False, string="Ready", help="Please select this when the delivery is ready to be processed.")
