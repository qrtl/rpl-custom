# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestSaleCommentTemplateExt(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.order = self.env["sale.order"].search([], limit=1)

