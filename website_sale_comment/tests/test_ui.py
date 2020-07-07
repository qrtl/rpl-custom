import odoo.tests

from odoo import api
from odoo.addons.website_sale_comment.controllers.main import WebsiteSaleForm
from odoo.addons.website.tools import MockRequest

#
# @odoo.tests.tagged('post_install', '-at_install')
# class TestWebsiteSaleComment(odoo.tests.TransactionCase):
#     ''' The goal of this method class is to test the Website Sale Comment on
#         the checkout.
#     '''
#     def setUp(self):
#         super(TestWebsiteSaleComment, self).setUp()
#         # self.default_address_values = {
#         #     'name': 'a res.partner address', 'email': 'email@email.email', 'street': 'ooo',
#         #     'city': 'ooo', 'country_id': self.country_id, 'submitted': 1,
#         # }
#
#     def _create_so(self, partner_id=None):
#         return self.env['sale.order'].create({
#             'partner_id': partner_id,
#             'website_id': self.website.id,
#             'order_line': [(0, 0, {
#                 'product_id': self.env['product.product'].create({'name': 'Product A', 'list_price': 100}).id,
#                 'name': 'Product A',
#             })]
#         })
#
#     def test_website_form_saleorder_tour(self):
#         sale_order = self._create_so(self.partner_id.id)
#         # self.env.ref("website_sale.extra_info").write({
#         #     'fixed_price': 2,
#         #     'free_over': True,
#         #     'amount': 10,
#         # })
#         print("sale_order",sale_order)
#         print("sale_order",sale_order)
#         print("sale_order",sale_order)
#         print("sale_order",sale_order)
#         print("sale_order",sale_order)
#         # "odoo.__DEBUG__.services['web_tour.tour'].run('shop')", "odoo.__DEBUG__.services['web_tour.tour'].tours.shop.ready", login = "admin")
#         # so = self._create_so(self.website.user_id.partner_id.id)
#
#         env = api.Environment(self.env.cr, self.env.user.id, {})
#         # # change also website env for `sale_get_order` to not change order partner_id
#         # with MockRequest(env, website=self.website.with_env(env), sale_order_id=sale_order.id):
#         #     # 1. Public user, new billing
#         #     # self.default_address_values['partner_id'] = -1
#         # self.x= {'Give us your feedback': 'Test Comment'}
#         # self.WebsiteSaleController.website_form_saleorder(**self.x)
#     # def test_03_demo_checkout(self):
#     # with MockRequest(env, website=self.website.with_env(env), sale_order_id=sale_order.id):
#
#             # self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('website_sale_comment_tour')", "odoo.__DEBUG__.services['web_tour.tour'].tours.website_sale_comment_tour.ready", login="admin")
#
@odoo.tests.tagged('post_install', '-at_install')
class TestUi(odoo.tests.HttpCase):

    def setUp(self):
        super(TestUi, self).setUp()
    # def test_01_admin_shop_tour(self):
    #     self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop')", "odoo.__DEBUG__.services['web_tour.tour'].tours.shop.ready", login="admin")
    #
    # def test_02_admin_checkout(self):
    #     self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('shop_buy_product')", "odoo.__DEBUG__.services['web_tour.tour'].tours.shop_buy_product.ready", login="admin")

    def test_03_demo_checkout(self):
        self.website = self.env['website'].browse(1)
        self.country_id = self.env['res.country'].search([], limit=1).id
        self.WebsiteSaleController = WebsiteSaleForm()
        self.partner_id = self.env.ref('base.partner_admin')
        sale_order = self._create_so(self.partner_id.id)
        print("sale_order",sale_order)
        print("sale_order",sale_order)
        print("sale_order",sale_order)
        print("sale_order",sale_order)
        print("sale_order.note2,",sale_order.note2)
        print("sale_order.note2,",sale_order.note2)
        self.phantom_js("/", "odoo.__DEBUG__.services['web_tour.tour'].run('website_sale_comment_tour')", "odoo.__DEBUG__.services['web_tour.tour'].tours.website_sale_comment_tour.ready", login="admin")

    def _create_so(self, partner_id=None):
        return self.env['sale.order'].create({
            'partner_id': partner_id,
            'website_id': self.website.id,
            'order_line': [(0, 0, {
                'product_id': self.env['product.product'].create({'name': 'Product A', 'list_price': 100}).id,
                'name': 'Product A',
            })]
        })
