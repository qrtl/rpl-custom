# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale


class Website(Website):
    @http.route()
    def index(self, **kw):
        """In case the home page is /shop, route the visitor to the login page.
        Without this adjustment, the shop page appears for the root node ('/') of the
        website.
        """
        homepage = request.website.homepage_id
        if homepage and homepage.url == "/shop":
            uid = request.env.user.id
            return http.local_redirect(self._login_redirect(uid), keep_hash=True)
        return super().index(**kw)


class WebsiteSale(WebsiteSale):
    @http.route(auth="user")
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        return super().shop(
            page=page, category=category, search=search, ppg=ppg, **post
        )

    @http.route(auth="user")
    def product(self, product, category="", search="", **kwargs):
        return super().product(
            product=product, category=category, search=search, **kwargs
        )
