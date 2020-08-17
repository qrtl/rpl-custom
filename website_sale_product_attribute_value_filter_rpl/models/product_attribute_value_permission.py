# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttributeValuePermission(models.Model):
    _name = "product.attribute.value.permission"

    product_id = fields.Many2one("product.product", string="Product", required=True)
    attribute_id = fields.Many2one(
        related="product_attribute_value_id.attribute_id", string="Attribute",
    )
    product_attribute_value_id = fields.Many2one(
        "product.attribute.value", string="Attribute Value", required=True,
    )
    allowed_country_group_ids = fields.Many2many(
        "res.country.group",
        "allowed_country_group_attribute_value_permission_rel",
        "product_attribute_value_permission_id",
        "res_country_group_id",
        string="Allowed Country Groups",
        help="If specified, the attribute value will be visible to "
        "customers from the countries in the specified group(s) in "
        "e-commerce.",
    )
    unallowed_country_group_ids = fields.Many2many(
        "res.country.group",
        "unallowed_country_group_attribute_value_permission_rel",
        "product_attribute_value_permission_id",
        "res_country_group_id",
        string="Unallowed Country Groups",
        help="If specified, the attribute value will not be visible to "
        "customers from the countries in the specified group(s) in "
        "e-commerce.",
    )
    allowed_country_ids = fields.Many2many(
        "res.country",
        "allowed_country_attribute_value_permission_rel",
        "product_attribute_value_permission_id",
        "res_country_id",
        string="Allowed Countries",
        help="If specified, the attribute value will be visible to "
        "customers from the countries in the specified countries in "
        "e-commerce.",
    )
    unallowed_country_ids = fields.Many2many(
        "res.country",
        "unallowed_country_attribute_value_permission_rel",
        "product_attribute_value_permission_id",
        "res_country_id",
        string="Unallowed Countries",
        help="If specified, the attribute value will not be visible to "
        "customers from the countries in the specified countries in "
        "e-commerce.",
    )
    allowed_partner_ids = fields.Many2many(
        "res.partner",
        "allowed_partner_attribute_value_permission_id_rel",
        "product_attribute_value_permission_id",
        "partner_id",
        string="Allowed Partners",
        help="If specified, the attribute value will always be visible to "
        "specified customer(s)",
    )
    unallowed_partner_ids = fields.Many2many(
        "res.partner",
        "unallowed_partner_attribute_value_permission_id_rel",
        "product_attribute_value_permission_id",
        "partner_id",
        string="Unallowed Partners",
        help="If specified, the attribute value will not be visible to "
        "specified customer(s)",
    )

    _sql_constraints = [
        (
            "unique_product_attribute",
            "unique(product_id, product_attribute_value_id)",
            _("The permission rule already exists."),
        )
    ]

    @api.constrains("allowed_partner_ids", "unallowed_partner_ids")
    def _check_partner_ids(self):
        if self.allowed_partner_ids and self.unallowed_partner_ids:
            concat_list = self.allowed_partner_ids + self.unallowed_partner_ids
            union_list = list(
                set(self.allowed_partner_ids + self.unallowed_partner_ids)
            )
            if len(concat_list) != len(union_list):
                raise ValidationError(
                    _(
                        "Partner can only be eirther allowed or unallowed "
                        "under the same rule."
                    )
                )

    @api.constrains("allowed_country_ids", "unallowed_country_ids")
    def _check_country_ids(self):
        if self.allowed_country_ids and self.unallowed_country_ids:
            concat_list = self.allowed_country_ids + self.unallowed_country_ids
            union_list = list(
                set(self.allowed_country_ids + self.unallowed_country_ids)
            )
            if len(concat_list) != len(union_list):
                raise ValidationError(
                    _(
                        "Country can only be either allowed or unallowed under"
                        " the same rule."
                    )
                )

    @api.constrains("allowed_country_group_ids", "unallowed_country_group_ids")
    def _check_country_group_ids(self):
        if self.allowed_country_group_ids and self.unallowed_country_group_ids:
            concat_list = (
                self.allowed_country_group_ids + self.unallowed_country_group_ids
            )
            union_list = list(
                set(self.allowed_country_group_ids + self.unallowed_country_group_ids)
            )
            if len(concat_list) != len(union_list):
                raise ValidationError(
                    _(
                        "Country group can only be either allowed or unallowed"
                        " under the same rule."
                    )
                )
