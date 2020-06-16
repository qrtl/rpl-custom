# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http, models
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

# Monkey Patching
# Overwrite the original checkout
# i.e. https://github.com/odoo/odoo/blob/5957aa317e8bb5b0041a1b5d8256cb3ff7d9fe42/addons/website_sale/controllers/main.py#L717-L742 # noqa
@http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
def checkout(self, **post):
    order = request.website.sale_get_order()

    redirection = self.checkout_redirection(order)
    if redirection:
        return redirection

    if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
        return request.redirect('/shop/address')

    for f in self._get_mandatory_billing_fields():
        if not order.partner_id[f]:
            return request.redirect('/shop/address?partner_id=%d' % order.partner_id.id)

    values = self.checkout_values(**post)

    # Modified by QTL >>>
    # Disable express checkout
    # if post.get('express'):
    #     return request.redirect('/shop/confirm_order')
    # Modified by QTL <<<

    values.update({'website_sale_order': order})

    # Avoid useless rendering if called in ajax
    if post.get('xhr'):
        return 'ok'
    return request.render("website_sale.checkout", values)

class WebsiteSaleHookCheckout(models.AbstractModel):
    _name = "website.sale.hook.checkout"
    _description = "Provide hook point for checkout method"

    def _register_hook(self):
        WebsiteSale.checkout = checkout
        return super(WebsiteSaleHookCheckout, self)._register_hook()
