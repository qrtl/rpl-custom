# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


# class WebsiteForum(WebsiteForum):
class WebsiteSale(WebsiteSale):
    @http.route(["/shop/terms"], type="http", auth="user", website=True)
    def terms(self, **kwargs):
        return super(WebsiteSale, self).terms(**kwargs)
