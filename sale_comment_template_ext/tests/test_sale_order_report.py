# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.sale_comment_template.tests.test_sale_order_report import (
    TestAccountInvoiceReport,
)


# Monkey Patching
# Overwrite the original test_comments_in_sale_order
def test_comments_in_sale_order(self):
    res = (
        self.env["ir.actions.report"]
        ._get_report_from_name("sale.report_saleorder")
        .render_qweb_html(self.sale_order.ids)
    )
    self.assertRegexpMatches(str(res[0]), self.before_comment.text)


TestAccountInvoiceReport.test_comments_in_sale_order = test_comments_in_sale_order
