# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ChangeProductionQty(models.TransientModel):
    _inherit = "change.production.qty"

    @api.multi
    def change_prod_qty(self):
        self = self.with_context(skip_action_assign=True)
        res = super().change_prod_qty()
        assign_manual_quants = self.env["assign.manual.quants"]
        fields_list = assign_manual_quants.fields_get().keys()
        # Following steps intends to automatically update the reserved
        # quantities of already selected lots.
        for wizard in self:
            for move in wizard.mo_id.move_raw_ids.filtered(lambda x: x.needs_lots):
                vals = assign_manual_quants.with_context(active_id=move.id).default_get(
                    fields_list
                )
                assign_quant_rec = assign_manual_quants.with_context(
                    active_id=move.id
                ).create(vals)
                for line in assign_quant_rec.quants_lines.filtered(
                    lambda x: x.selected
                ):
                    # Below steps should be consistent with
                    # _onchange_selected() of assign.manual.quants
                    line.qty = 0.0
                    quant_qty = line.on_hand - line.reserved
                    remaining_qty = line.assign_wizard.move_qty
                    line.qty = min(quant_qty, remaining_qty)
                assign_quant_rec.assign_quants()
        return res
