# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_is_zero


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    component_lot_filter = fields.Char()
    need_component_lot_filter = fields.Boolean(compute="_compute_need_component_lot_filter")
    show_action_assign = fields.Boolean(compute="_compute_show_action_assign")

    def _compute_need_component_lot_filter(self):
        for production in self:
            if production.move_raw_ids.filtered(lambda x: x.product_id.lot_restriction):
                production.need_component_lot_filter = True

    def _compute_show_action_assign(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for production in self:
            show_action_assign = True
            for move in production.move_raw_ids.filtered(lambda x: x.product_id.lot_restriction):
                if not float_is_zero(move.quantity_done - move.product_uom_qty, precision_digits=precision):
                    show_action_assign = False
                    break
            production.show_action_assign = show_action_assign
