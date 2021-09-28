# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    active = fields.Boolean(default=True)

    @api.constrains("active", "quant_ids")
    def _check_quant_ids(self):
        if not self.active and self.quant_ids:
            raise ValidationError(
                _("Lots/serials with product move history cannot be archived.")
            )
