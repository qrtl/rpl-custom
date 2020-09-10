# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSaleForm


class WebsiteSaleForm(WebsiteSaleForm):
    @http.route(
        "/website_form/shop.sale.order",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def website_form_saleorder(self, **kwargs):
        order = request.website.sale_get_order()
        note_list = []
        if kwargs.get("increase_refrigerant") and order:
            note_list.append(_("Increase due to refrigerant (the box to be used for shipping will be one size larger)"))
        if kwargs.get("Give us your feedback") and order:
            remarks = kwargs.get("Give us your feedback")
            note_list.append(_("Customer Remarks: ") + remarks)
        order.write({"note2": "<br>".join(note_list)})
        return super(WebsiteSaleForm, self).website_form_saleorder(**kwargs)
