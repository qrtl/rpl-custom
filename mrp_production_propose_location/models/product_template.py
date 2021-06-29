# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    use_alt_location_dest = fields.Boolean(
        "Use Alt. Destination Location",
        help="If selected, destination location will be proposed from the "
        "alternative destinaton location of the relevant operation type.",
    )
