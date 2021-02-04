# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import html2text

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    
