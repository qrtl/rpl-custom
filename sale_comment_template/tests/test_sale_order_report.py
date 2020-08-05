# Copyright 2017 Simone Rubino - Agile Business Group
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import odoo.tests
from odoo.tests.common import TransactionCase


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class TestAccountInvoiceReport(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestAccountInvoiceReport, self).setUp()
        self.base_comment_model = self.env['base.comment.template']
        self.before_comment = self._create_comment('before_lines')
        self.after_comment = self._create_comment('after_lines')
        self.partner_id = self.env['res.partner'].create({
            'name': 'Partner Test'
        })
        # QRTL EDIT:
        # Change to another sales order since mrp_subcontracting added
        # "Make to order" route to "[FURN_8888] Office Lamp" which causes
        # "No procurement rule found" error when confirming the sale order.
        # https://github.com/qrtl/rpl-custom/pull/75/files#diff-0eafdf1385d96e12f82a2ff7847b1571R27-R29 # noqa
        # self.sale_order = self.env.ref('sale.sale_order_7')
        self.sale_order = self.env.ref('sale.sale_order_3')
        # Trigger qty_to_invoice again
        for order_line in self.sale_order.order_line:
            order_line.product_id.invoice_policy = 'order'
        self.sale_order.action_confirm()

        self.sale_order.update({
            'comment_template1_id': self.before_comment.id,
            'comment_template2_id': self.after_comment.id
        })
        self.sale_order._set_note1()
        self.sale_order._set_note2()

    def _create_comment(self, position):
        return self.base_comment_model.create({
            'name': 'Comment ' + position,
            'position': position,
            'text': 'Text ' + position
        })

    def test_comments_in_sale_order(self):
        res = self.env['ir.actions.report']._get_report_from_name(
            'sale.report_saleorder'
        ).render_qweb_html(self.sale_order.ids)
        self.assertRegexpMatches(str(res[0]), self.before_comment.text)
        self.assertRegexpMatches(str(res[0]), self.after_comment.text)

    def test_comments_in_generated_invoice(self):
        invoice_ids = self.sale_order.action_invoice_create()
        invoice = self.env['account.invoice'].browse(invoice_ids)
        self.assertEqual(
            invoice.comment_template1_id,
            self.sale_order.comment_template1_id,
        )
        self.assertEqual(
            invoice.comment_template2_id,
            self.sale_order.comment_template2_id,
        )

    def test_onchange_partner_id(self):
        self.partner_id.comment_template_id = self.after_comment.id
        vals = {
            'partner_id': self.partner_id.id,
        }
        new_sale = self.env['sale.order'].new(vals)
        new_sale.onchange_partner_id_sale_comment()
        sale_dict = new_sale._convert_to_write(new_sale._cache)
        new_sale = self.env['sale.order'].create(sale_dict)
        self.assertEqual(new_sale.comment_template2_id, self.after_comment)
        self.partner_id.comment_template_id = self.before_comment.id
        new_sale = self.env['sale.order'].new(vals)
        new_sale.onchange_partner_id_sale_comment()
        sale_dict = new_sale._convert_to_write(new_sale._cache)
        new_sale = self.env['sale.order'].create(sale_dict)
        self.assertEqual(new_sale.comment_template1_id, self.before_comment)
