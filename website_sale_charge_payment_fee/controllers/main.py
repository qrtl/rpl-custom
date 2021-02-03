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
        [
            "/shop/payment/transaction/",
            "/shop/payment/transaction/<int:so_id>",
            "/shop/payment/transaction/<int:so_id>/<string:access_token>",
        ],
        type="json",
        auth="public",
        website=True,
    )
    def payment_transaction(
        self,
        acquirer_id,
        save_token=False,
        so_id=None,
        access_token=None,
        token=None,
        **kwargs
    ):
        # Borrow the logic from standard Odoo to check against acquirer_id and order
        # https://github.com/odoo/odoo/blob/aba9056e7baa58decf147313678ad9d1f4522dee/addons/website_sale/controllers/main.py#L887-L910 # noqa
        # Ensure a payment acquirer is selected
        if not acquirer_id:
            return False

        try:
            acquirer_id = int(acquirer_id)
        except:
            return False

        # Retrieve the sale order
        if so_id:
            env = request.env["sale.order"]
            domain = [("id", "=", so_id)]
            if access_token:
                env = env.sudo()
                domain.append(("access_token", "=", access_token))
            order = env.search(domain, limit=1)
        else:
            order = request.website.sale_get_order()

        # Ensure there is something to proceed
        if not order or (order and not order.order_line):
            return False

        assert order.partner_id.id != request.website.partner_id.id

        # Update payment fee line
        payment_acquirer = request.env["payment.acquirer"].browse(acquirer_id)
        order.sudo().update_fee_line(payment_acquirer.sudo())
        return super(WebsiteSaleFee, self).payment_transaction(
            acquirer_id,
            save_token=save_token,
            so_id=so_id,
            access_token=access_token,
            token=token,
            **kwargs
        )
