from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSaleExtended(WebsiteSale):

    # Inherit method for implement Price Filter and Brand Filter
    def _get_search_domain(self, search, category, attrib_values):
        domain = super(WebsiteSaleExtended, self)._get_search_domain(
            search=search, category=category,
            attrib_values=attrib_values)
        if category and category.sudo().partner_ids and (
            request.env.user.has_group('base.group_public') or
            request.env.user.has_group('base.group_portal')):
            partner_id = request.env.user.commercial_partner_id
            domain += ["|",
                       ("is_public", "=", True),
                       ("public_categ_ids", "in", partner_id.category_ids.ids)]
