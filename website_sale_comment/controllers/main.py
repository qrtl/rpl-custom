# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.http import request
from odoo.tools import html2plaintext, plaintext2html

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
        request.session["Give us your feedback"] = kwargs.get("Give us your feedback")
        note_list = []
        if kwargs.get("Give us your feedback") and order:
            remarks = kwargs.get("Give us your feedback")
            note_list.append(_("Customer Remarks: ") + remarks)
        if request.env["sale.order"]._default_note():
            note_list.insert(
                0, (plaintext2html(request.env["sale.order"]._default_note()))
            )
        note = "<br>".join(note_list)
        order.write({"note": html2plaintext(note), "note2": remarks})
        return super(WebsiteSaleForm, self).website_form_saleorder(**kwargs)
