# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    note2 = fields.Html( #)
    #     default=lambda self:self.env["sale.order.line"]group_id.note2
        default=lambda self:self.group_id.sale_id.note2
    )
