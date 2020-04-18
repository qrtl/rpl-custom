# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def sale_product_domain(self):
        """ Even if a product belongs to a restricted category, the product
            should still show if it also belongs to a non-restricted category.
        """
        res = super(Website, self).sale_product_domain()
        user = self.env.user
        if user.has_group("base.group_public") or user.has_group("base.group_portal"):
            public_categ = self.env["product.public.category"]
            restricted_categs = public_categ.browse()
            categs = user.commercial_partner_id.public_category_ids
            for categ in categs:
                restricted_categs += categ.get_offsprings()
            allowed_categs = public_categ.search([]) - restricted_categs
            res += [
                ("public_categ_ids", "in", allowed_categs.ids),
            ]
        return res
