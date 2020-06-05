# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values, errors, error_msg = super(WebsiteSale, self).values_postprocess(order, mode, values, errors, error_msg)
        # We do not want to make a change on existing shipping address
        if mode == ('new', 'shipping') and order.partner_id.commercial_partner_id.hide_self_for_children:
            new_values["hide_parent"] = True
        return new_values, errors, error_msg
