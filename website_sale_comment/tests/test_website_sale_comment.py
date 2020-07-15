# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class TestUi(odoo.tests.HttpCase):
    def setUp(self):
        super(TestUi, self).setUp()

    def test_website_sale_comment(self):
        # Enable Extra Step option from Customize Menu
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].run("
            "'enable_extra_step_setting')",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].tours.enable_extra_step_setting.ready",
            login="admin",
        )


        # Checking the website comment flow
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].run('website_sale_comment_tour_sale')",
            "odoo.__DEBUG__.services["
            "'web_tour.tour'].tours.website_sale_comment_tour_sale.ready",
            login="admin",
        )
        partner_id = self.env.ref('base.partner_admin').id
        sale_order = self.env['sale.order'].search([
            ('partner_id', '=', partner_id)], limit=1)

        # Compare the SaleOrder Note2 Value which is create by tour test-case
        self.assertEqual(
            sale_order.note2,
            '<p>Customer Remarks: Test Feedback Comment</p>',
            'Sale Order Note2 does not Match with the value.'
        )
