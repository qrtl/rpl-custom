# Copyright 2021-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    acquirer_id = fields.Many2one(
        "payment.acquirer",
        string="Acquirer",
        help="The selection here may affect the presentation of the printed invoice "
        "(domestic).",
    )
    is_direct_debit = fields.Boolean(related="acquirer_id.is_direct_debit")

    def _get_onchange_create(self):
        res = super()._get_onchange_create()
        res["_onchange_partner_id"].append("acquirer_id")
        return res

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        super()._onchange_partner_id()
        if self.transaction_ids:
            self.acquirer_id = self.transaction_ids[0].acquirer_id
        else:
            self.acquirer_id = self.commercial_partner_id.acquirer_ids[:1]
