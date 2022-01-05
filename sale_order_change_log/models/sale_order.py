# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # product_id_temp = fields.Many2one(related="partner_id.country_id", store=True,)
    # product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict') #origin
    # temp_product_id = fields.Char('product.product', string='Temp Product', track_visibility="onchange", readonly=True)
    # product_uom_qt_temp = fields.Char(related="partner_id.country_id.code", store=True,)
    # product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0) #origin
    # temp_product_uom_qty = fields.Float(string='Temp Ordered Quantity', track_visibility="onchange", readonly=True)

    # origin from odoo>addons>sale>models>sale.py line220
    # amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='onchange', track_sequence=5)
    temp_product_id = fields.Char(string='Temp Product', store=True, readonly=True, track_visibility='onchange', track_sequence=5)
    temp_product_uom_qty = fields.Float(string='Temp Ordered Quantity', store=True, readonly=True, track_visibility='onchange', track_sequence=5)

    # ↓compute部分を削除する前
    # temp_product_id = fields.Char(string='Temp Product', store=True, readonly=True, compute='_change_result_product', track_visibility='onchange', track_sequence=5)
    # temp_product_uom_qty = fields.Float(string='Temp Ordered Quantity', store=True, readonly=True, compute='_change_result_qty', track_visibility='onchange', track_sequence=5)


    # @api.depends('order_line.price_total')
    # def _change_result_product(self):
    #     """
    #     Compute the change result for the SO products.
    #     """
    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         order.update({
    #             'amount_untaxed': amount_untaxed,
    #             'amount_tax': amount_tax,
    #             'amount_total': amount_untaxed + amount_tax,
    #         })


    # @api.depends('order_line.price_total')
    # def _change_result_qty(self):
    #     """
    #     Compute the change result for the SO qty.
    #     """
    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         order.update({
    #             'amount_untaxed': amount_untaxed,
    #             'amount_tax': amount_tax,
    #             'amount_total': amount_untaxed + amount_tax,
    #         })

    # origin
    # @api.depends('order_line.price_total')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         order.update({
    #             'amount_untaxed': amount_untaxed,
    #             'amount_tax': amount_tax,
    #             'amount_total': amount_untaxed + amount_tax,
    #         })

