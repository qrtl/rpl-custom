# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    product_tracking = fields.Selection(related="product_id.tracking")
    new_lot_id = fields.Many2one("stock.production.lot", "New Lot", copy=False)

    def action_create_new_lot(self):
        for rec in self:
            if not rec.new_lot_id:
                date_finished = fields.Datetime.context_timestamp(
                    self, rec.date_planned_finished
                ).strftime("%Y-%m-%d")
                rec.new_lot_id = self.env['stock.production.lot'].create({
                    "product_id": rec.product_id.id,
                    "date_finished": date_finished,
                })

    #TODO update date_finished field of the linked lot with date_finished of the production when it's marked as done.
