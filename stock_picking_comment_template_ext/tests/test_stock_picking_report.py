# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.stock_picking_comment_template.tests.test_stock_picking_report import (
    TestStockPickingReport,
)


# Monkey Patching
# Overwrite the original test_comments_in_picking
def test_comments_in_picking(self):
    res = (
        self.env["ir.actions.report"]
        ._get_report_from_name("stock.report_picking")
        .render_qweb_html(self.picking.ids)
    )
    self.assertRegexpMatches(str(res[0]), self.before_comment.text)


TestStockPickingReport.test_comments_in_picking = test_comments_in_picking
