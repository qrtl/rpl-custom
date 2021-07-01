# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.onchange("picking_type_id", "product_id")
    def onchange_picking_type(self):
        super().onchange_picking_type()
        if (
            self.product_id.use_alt_location_dest
            and self.picking_type_id.alt_location_dest_id
        ):
            self.location_dest_id = self.picking_type_id.alt_location_dest_id.id
