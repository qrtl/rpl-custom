# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_restriction = fields.Boolean(related="product_id.lot_restriction")

    def _action_assign(self):
        # Skip _action_assign() in case of production qty change.
        if not self._context.get("skip_action_assign", False):
            super()._action_assign()
