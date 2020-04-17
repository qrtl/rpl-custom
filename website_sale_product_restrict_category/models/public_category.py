# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = "product.public.category"

    def get_all_parents(self):
        self.ensure_one()
        res = self.env['product.public.category'].browse(None)
        if self.parent_id:
            res += self.parent_id + self.parent_id.get_all_parents()
        return res

    def get_all_children(self):
        self.ensure_one()
        res = self.env['product.public.category'].browse(None)
        for child in self.child_id:
            res += child + child.get_all_children()
        return res

    partner_ids = fields.Many2many(
        "res.partner",
        string="Partners")

    @api.model
    def create(self, vals):
        res = super(ProductCategory, self).create(vals)
        if vals.get('partner_ids'):
            partner_ids = self.env['res.partner'].browse(vals.get(
                'partner_ids')[0][2])
            for partner in partner_ids:
                child_category_ids = set(res.get_all_children())
                for child_category in child_category_ids:
                    partner_ids = child_category.partner_ids and \
                                  set(child_category.partner_ids + partner) \
                                  or partner
                    child_category.write({'partner_ids': [(6, 0,
                                                           partner_ids.ids)]})
                public_category = partner.mapped(
                    'public_category_ids') and partner.mapped(
                    'public_category_ids').ids or []
                if res.id not in public_category:
                    partner.write({'public_category_ids': [(4, res.id)]})
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductCategory, self).write(vals)
        if vals.get('partner_ids'):
            partner_ids = self.env['res.partner'].browse(vals.get('partner_ids')[0][2])
            for partner in partner_ids:
                child_category_ids = set(self.get_all_children())
                for child_category in child_category_ids:
                    partner_ids = child_category.partner_ids and \
                                  child_category.partner_ids + partner \
                                  or partner
                    child_category.write({'partner_ids': [(6, 0,
                                                           partner_ids.ids)]})
                public_category = partner.mapped(
                    'public_category_ids') and partner.mapped(
                    'public_category_ids').ids or []
                if self.id not in public_category:
                    partner.write({'public_category_ids': [(4, self.id)]})
        return res
