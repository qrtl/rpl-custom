# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    partner_ids = fields.Many2many("res.partner", string="Partners to Hide From")

    def get_offsprings(self):
        """ Returned value includes the originating category itself.
        """
        self.ensure_one()
        res = self
        for child in self.child_id:
            res += child.get_offsprings()
        return res
