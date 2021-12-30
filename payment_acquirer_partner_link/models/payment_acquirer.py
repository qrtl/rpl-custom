# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    partner_ids = fields.Many2many("res.partner", string="Partners")
    is_direct_debit = fields.Boolean(
        "Direct Debit",
        help="Select this if the aquirer is for direct debit. This selection may "
        "eventually affect the presentation of the printed invoice.",
    )
