# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route(
        ['/shop/country_infos/<model("res.country"):country>'],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def country_infos(self, country, mode, **kw):
        res = super(WebsiteSale, self).country_infos(country, mode, **kw)
        if country.online_address_format:
            res["fields"] = country.get_online_address_fields()
        return res
