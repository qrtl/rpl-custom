# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    country = fields.Many2one(
        related="partner_id.country_id", readonly=True, store=True,
    )
    country_code = fields.Char(related="partner_id.country_id.code")
