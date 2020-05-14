# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSaleForm


class WebsiteSaleForm(WebsiteSaleForm):

    @http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **kwargs):
        order = request.website.sale_get_order()
        if kwargs.get('Give us your feedback') and order:
            remarks = kwargs.get('Give us your feedback')
            order.write({'note2': remarks})
            kwargs.pop('Give us your feedback')
        return super(WebsiteSaleForm, self).website_form_saleorder(**kwargs)
