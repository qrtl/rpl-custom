# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Post(models.Model):
    _inherit = "product.template"

    is_public = fields.Boolean(compute="_compute_is_public", store=True)

    @api.depends(
        "public_categ_ids", "public_categ_ids.partner_ids",
    )
    def _compute_is_public(self):
        """ This Method check the does e-commerce category contains
         the partners or not.
        """
        for product in self:
            if product.public_categ_ids.mapped("partner_ids"):
                product.is_public = False
            else:
                product.is_public = True
