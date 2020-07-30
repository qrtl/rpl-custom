# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_price = fields.Monetary(
        string="Delivery Price (Tax Included)",
        copy=False,
        help="Takes the delivery price from related sale order when delivery "
        "is created. User can manually adjust the amount as necessary.",
    )

    @api.multi
    def _compute_amount_all(self):
        super(StockPicking, self)._compute_amount_all()
        for pick in self:
            pick.amount_total += pick.delivery_price
