# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    hide_self_for_children = fields.Boolean(
        help="If selected, 'Hide Parent' will be selected by default for the "
        "delivery addresses created through the eCommerce interface."
    )
