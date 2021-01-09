# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def action_assign_component(self):
        for production in self:
            production.move_raw_ids._action_assign_component()
        return True
