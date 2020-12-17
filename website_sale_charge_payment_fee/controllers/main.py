# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2020 AITIC S.A.S
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleFee(WebsiteSale):
    @http.route(
        ["/shop/payment"], type="http", auth="public", website=True, sitemap=False
    )
    def payment(self, **post):
        res = super(WebsiteSaleFee, self).payment(**post)
        values = res.qcontext
        order = request.website.sale_get_order()
        payment_fee_id = post.get("payment_fee_id")
        checked_pm_id = post.get("pm_id")
        if checked_pm_id:
            values["checked_pm_id"] = int(checked_pm_id)
        if payment_fee_id or "acquirers" in values:
            # If 'acquirers' in values, default behaviour when acquirers are
            # present, we update the order with the first one
            # (see 'payment' template)
            # If payment_fee_id, it means user selected it
            # (see website_sale_fee.js)
            if payment_fee_id:
                selected_acquirer = request.env["payment.acquirer"].browse(
                    int(payment_fee_id)
                )
            else:
                selected_acquirer = values["acquirers"][0]
            values["selected_acquirer"] = selected_acquirer
            order.sudo().update_fee_line(selected_acquirer.sudo())
            return request.render("website_sale.payment", values)
        return res

    @http.route(
        ["/shop/update_acquirer"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def update_acquirer(self, **post):
        order = request.website.sale_get_order()
        acquirer_id = post.get("acquirer_id")
        if acquirer_id:
            acquirer = request.env["payment.acquirer"].browse(int(acquirer_id))
            order.sudo().update_fee_line(acquirer.sudo())
        if "carrier_id" not in post:
            post["carrier_id"] = order.carrier_id.id
        results = self._update_website_sale_delivery_return(order, **post)
        results["amount_payment_fee"] = order.amount_payment_fee
        return results
