# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero


filter_length = 8

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
                if not float_is_zero(move.product_uom_qty - move.reserved_availability, precision_digits=precision):
                    show_action_assign = False
                    break
            production.show_action_assign = show_action_assign

    @api.constrains("component_lot_filter")
    def _check_component_lot_filter(self):
        for production in self:
            if production.component_lot_filter and len(production.component_lot_filter) != filter_length:
                    raise ValidationError(
                        _("Component Lot Filter must be 8-character long.")
                    )

    @api.multi
    def open_produce_product(self):
        self.ensure_one()
        if self.need_component_lot_filter:
            if not self.component_lot_filter:
                raise UserError(_("Please set the Component Lot Filter and select lots accordingly"))
            lots = self.move_raw_ids.filtered(lambda x: x.product_id.lot_restriction).mapped("move_line_ids").mapped("lot_id")
            if not lots:
                raise UserError(_("Please select lots according to the Component Lot Filter"))
            for lot in lots:
                if lot.ref[:filter_length] != self.component_lot_filter:
                    raise UserError(
                        _("There is an inconsistency between the Component Lot Filter and selected lot.")
                    )
        for move in self.move_raw_ids:
            if len(move.move_line_ids) > 1:
                raise UserError(
                    _("It is not allowed to use more than one lot per component: %s") % (move.product_id.display_name)
                )
        return super().open_produce_product()
