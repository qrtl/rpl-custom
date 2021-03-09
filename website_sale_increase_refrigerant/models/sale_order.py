# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    increase_refrigerant = fields.Boolean(
        "Increase Refrigerant",
    )
