# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    alt_location_dest_id = fields.Many2one(
        "stock.location",
        "Alt. Destination Location",
        help="This location may be proposed as the destination location in a "
        "manufacturing order if it's indicated to do so in the produced product.",
    )
