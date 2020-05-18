# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.account_invoice_comment_template.tests.test_account_invoice_report import (  # noqa
    TestAccountInvoiceReport,
)


# Monkey Patching
# Overwrite the original test_comments_in_invoice
def test_comments_in_invoice(self):
    res = (
        self.env["ir.actions.report"]
        ._get_report_from_name("account.report_invoice")
        .render_qweb_html(self.invoice.ids)
    )
    self.assertRegexpMatches(str(res[0]), self.before_comment.text)


TestAccountInvoiceReport.test_comments_in_invoice = test_comments_in_invoice
