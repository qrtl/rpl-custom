# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    label_ref = fields.Char(
        "Label Reference",
        compute="_compute_label_ref",
        inverse="_inverse_label_ref",
        store=True,
        help="The value set here will be used as 'REF' in product label " "print.",
    )

    @api.depends("product_variant_ids", "product_variant_ids.label_ref")
    def _compute_label_ref(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.label_ref = template.product_variant_ids.label_ref
        for template in self - unique_variants:
            template.label_ref = ""

    def _inverse_label_ref(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.label_ref = self.label_ref
