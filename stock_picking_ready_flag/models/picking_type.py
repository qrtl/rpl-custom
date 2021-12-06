# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    def get_action_picking_tree_ready(self):
        if self.code != "outgoing":
            return self._get_action("stock.action_picking_tree_ready")
        return self._get_action(
            "stock_picking_ready_flag.action_picking_tree_ready_to_ship"
        )
