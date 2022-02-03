# Copyright 2021-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        vals = super()._get_shop_payment_values(order, **kwargs)
        # Override the acquirers val in case an acquirer linked to the partner can be
        # found.
        # We have the conditions of ('specific_countries', '=', True) and
        # ('country_ids', '=', False), to avoid the overlap of the the conditions with
        # the standard method.
        domain = expression.AND(
            [
                [
                    ("website_published", "=", True),
                    ("company_id", "=", order.company_id.id),
                    ("specific_countries", "=", True),
                    ("country_ids", "=", False),
                    ("partner_ids", "in", [order.partner_id.commercial_partner_id.id]),
                    ("payment_flow", "=", "form"),
                    ("view_template_id", "!=", False),
                ],
                [
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", request.website.id),
                ],
            ]
        )
        acquirers = request.env["payment.acquirer"].search(domain)
        if acquirers:
            # The acquirer found is expected to be for direct debits, therefore we
            # assume that no token should be available.
            vals["acquirers"] = acquirers
            vals["tokens"] = False
        return vals
