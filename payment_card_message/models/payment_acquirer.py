# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit="payment.acquirer"

    card_msg = fields.Html(
        "Card Message", translate=True,
        help="Message displayed on the payment card in portal/eCommerce "
        "checkout screen."
    )
