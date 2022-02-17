# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def payment(self, **post):
        res = super(WebsiteSale, self).payment(**post)
        order = request.website.sale_get_order()
        order.date_order = datetime.now()
        return res
