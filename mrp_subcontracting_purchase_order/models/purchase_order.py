# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    subcontract_production_ids = fields.One2many(
        "mrp.production",
        "purchase_order_id",
        "Subcontract Production Orders",
        readonly=True,
    )
    subcontract_production_count = fields.Integer(
        compute="_compute_subcontract_production_count"
    )

    @api.multi
    def action_view_mrp(self):
        productions = self.mapped("subcontract_production_ids")
        action = self.env.ref("mrp.mrp_production_action").read()[0]
        if len(productions) > 1:
            action["domain"] = [("id", "in", productions.ids)]
        elif len(productions) == 1:
            form_view = [(self.env.ref("mrp.mrp_production_form_view").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = productions.ids[0]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    @api.multi
    def _compute_subcontract_production_count(self):
        for order in self:
            order.subcontract_production_count = len(order.subcontract_production_ids)
