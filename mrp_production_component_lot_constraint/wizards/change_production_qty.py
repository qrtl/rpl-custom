# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ChangeProductionQty(models.TransientModel):
    _inherit = "change.production.qty"

    def _get_move_lot_quants(self):
        self.ensure_one()
        res = {}
        for move in self.mo_id.move_raw_ids:
            if move.needs_lots:
                lots = move.move_line_ids.mapped("lot_id")
                quants = self.env["stock.quant"].search(
                    [
                        ("location_id", "child_of", move.location_id.id),
                        ("product_id", "=", move.product_id.id),
                        ("quantity", ">", 0),
                        ("lot_id", "in", lots.ids),
                    ]
                )
                res[move.id] = quants
        return res

    @api.model
    def _refresh_quant_line_qty(self, quant_line):
        quant_line.selected = False
        quant_line._onchange_selected()
        quant_line.selected = True
        quant_line._onchange_selected()

    @api.multi
    def change_prod_qty(self):
        self.ensure_one()
        # For later processing, form a dict of the moves and the assigned quants before
        # the moves are unreserved, while unreserving them.
        move_lot_quants = self._get_move_lot_quants()
        # Prevent assigning unwanted quants with skip_action_assign context.
        self = self.with_context(skip_action_assign=True)
        res = super().change_prod_qty()
        assign_manual_quants = self.env["assign.manual.quants"]
        fields_list = assign_manual_quants.fields_get().keys()
        # Following steps intends to redo the reservation of the quants that had been
        # assigned before being unreserved.
        for move in self.mo_id.move_raw_ids:
            if move.product_id.type == "product":
                vals = assign_manual_quants.with_context(active_id=move.id).default_get(
                    fields_list
                )
                assign_quant_rec = assign_manual_quants.with_context(
                    active_id=move.id,
                ).create(vals)
                if move.needs_lots:
                    for quant in move_lot_quants[move.id]:
                        for line in assign_quant_rec.quants_lines.filtered(
                            lambda x: x.quant_id == quant
                        ):
                            self._refresh_quant_line_qty(line)
                else:
                    # Taking following steps since move._action_assign() does not seem
                    # to work here.
                    line = assign_quant_rec.quants_lines[:1]
                    if line:
                        self._refresh_quant_line_qty(line)
                assign_quant_rec.assign_quants()
            else:
                # For 'consu' type.
                # FIXME This _action_assign() does not seem to work for some reason.
                move._action_assign()
        return res
