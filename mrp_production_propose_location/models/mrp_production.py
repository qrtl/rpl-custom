# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    # @api.model
    # def _get_default_location_dest_id(self):
    #     location = False
    #     if self._context.get('default_picking_type_id'):
    #         location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_dest_id
    #     if not location:
    #         location = self.env.ref('stock.stock_location_stock', raise_if_not_found=False)
    #         try:
    #             location.check_access_rule('read')
    #         except (AttributeError, AccessError):
    #             location = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)], limit=1).lot_stock_id
    #     return location and location.id or False

    @api.onchange("picking_type_id", "product_id")
    def onchange_picking_type(self):
        super().onchange_picking_type()
        if self.product_id.use_alt_location_dest and self.picking_type_id.alt_location_dest_id:
            self.location_dest_id = self.picking_type_id.alt_location_dest_id.id
    # @api.onchange('picking_type_id', 'routing_id')
    # def onchange_picking_type(self):
    #     location = self.env.ref('stock.stock_location_stock')
    #     try:
    #         location.check_access_rule('read')
    #     except (AttributeError, AccessError):
    #         location = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)], limit=1).lot_stock_id
    #     self.location_src_id = self.routing_id.location_id.id or self.picking_type_id.default_location_src_id.id or location.id
    #     self.location_dest_id = self.picking_type_id.default_location_dest_id.id or location.id
