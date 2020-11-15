# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    product_tracking = fields.Selection(related="product_id.tracking")
    new_lot_id = fields.Many2one("stock.production.lot", "New Lot")

    def action_create_new_lot(self):
        for rec in self:
            if not rec.new_lot_id:
                rec.new_lot_id = self.env['stock.production.lot'].create({
                    "company_id": self.env.user.company_id.id,
                    'product_id': rec.product_id.id
                })
