# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from ..models.mrp_production import filter_length


class AssignManualQuants(models.TransientModel):
    _inherit = "assign.manual.quants"

    @api.multi
    def assign_quants(self):
        res = super().assign_quants()
        move = self.move_id
        production = move.raw_material_production_id
        if move.lot_restriction and production and not production.component_lot_filter:
            selected_lot = move.move_line_ids.mapped("lot_id")[:1]
            if selected_lot:
                production.component_lot_filter = selected_lot.ref[:filter_length]
        return res

    @api.model
    def _domain_for_available_quants(self, move):
        domain = super()._domain_for_available_quants(move)
        production = move.raw_material_production_id
        if not production:
            return domain
        if production.component_lot_filter and move.lot_restriction:
            lots = self.env["stock.production.lot"].search(
                [
                    ("product_id", "=", move.product_id.id),
                    ("ref", "=ilike", production.component_lot_filter + "%"),
                ]
            )
            reserved_lots = move.move_line_ids.mapped("lot_id")
            lots += reserved_lots
            domain.append(("lot_id", "in", lots.ids))
        return domain
