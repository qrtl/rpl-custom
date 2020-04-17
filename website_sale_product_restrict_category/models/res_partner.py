# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    public_category_ids = fields.Many2many(
        "product.public.category", string="Product Category"
    )

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if vals.get("public_category_ids"):
            public_category_ids = self.env["product.public.category"].browse(
                vals.get("public_category_ids")[0][2]
            )
            for category in public_category_ids:
                partner_ids = (
                    category.mapped("partner_ids")
                    and category.mapped("partner_ids").ids
                )
                if res.id not in partner_ids:
                    category.write({"partner_ids": [(4, res.id)]})
        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if vals.get("product.public.category"):
            partner_ids = self.env["product.public.category"].browse(
                vals.get("public_category_ids")[0][2]
            )
            for partner in partner_ids:
                partner_ids = (
                    partner.mapped("partner_ids") and partner.mapped("partner_ids").ids
                )
                if self.id not in partner_ids:
                    partner.write({"partner_ids": [(4, self.id)]})
        return res
