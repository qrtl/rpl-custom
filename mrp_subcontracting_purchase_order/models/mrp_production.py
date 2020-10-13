# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    purchase_order_id = fields.Many2one('purchase.order', 'Subcontract Purchase Order', readonly=True)
