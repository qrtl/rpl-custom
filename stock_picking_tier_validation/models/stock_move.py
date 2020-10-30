# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.constrains('state', 'picking_id.review_ids', 'picking_id.review_ids.status')
    def _check_review(self):
        if self.state == "done" and not self.picking_id.validated:
            raise ValidationError(_('This picking needs to be validated.'))
