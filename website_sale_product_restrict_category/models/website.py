# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def sale_product_domain(self):
        domain = super(Website, self).sale_product_domain()
        if self.env.user.has_group('base.group_public') or \
            self.env.user.has_group('base.group_portal'):
            public_category_ids = \
                self.env.user.commercial_partner_id.public_category_ids
            domain += ["|",
                       ("is_public", "=", True),
                       ("public_categ_ids", "in", public_category_ids.ids)]
        return domain
