# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    base_date = fields.Integer("Base Date")
    weekday_delta = fields.Integer("Weekday Delta", help="Base weekday is Monday",)
    month_delta = fields.Integer("Month Delta")
    day_delta = fields.Integer("Day Delta")
