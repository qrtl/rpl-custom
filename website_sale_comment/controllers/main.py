# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route(["/website/notes"], type="json", auth="public", website=True)
    def order_notes(self, note2="", **post):
        order = request.website.sale_get_order()
        order.sudo().write({"note2": note2})
        return True
