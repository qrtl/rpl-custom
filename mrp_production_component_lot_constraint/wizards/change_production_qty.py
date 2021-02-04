# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ChangeProductionQty(models.TransientModel):
    _inherit = "change.production.qty"

    @api.multi
    def change_prod_qty(self):
        self = self.with_context(skip_action_assign=True)
        return super().change_prod_qty()
