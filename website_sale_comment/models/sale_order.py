# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.tools import html2plaintext


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_note_plaintext(self):
        self.ensure_one()
        return html2plaintext(self.note2)
