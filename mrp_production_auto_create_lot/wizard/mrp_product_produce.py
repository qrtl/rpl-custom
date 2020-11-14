# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    auto_create_lot = fields.Boolean(related="production_id.product_id.auto_create_lot")

    @api.multi
    def do_produce(self):
        if self.production_id.product_id.auto_create_lot and not self.lot_id:
            self.lot_id = self.env['stock.production.lot'].create({
                'product_id': self.production_id.product_id.id,
            })
        return super().do_produce()
