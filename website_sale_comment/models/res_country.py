# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    increase_refrigerant_visible = fields.Boolean(
        'Show "Increase Refrigerant" option',
        default=True,
    )
