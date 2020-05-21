# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    luxis_status = fields.Char(string='Status')
    luxis_payment_id = fields.Char(string='Payment ID')
    luxis_ip_address = fields.Char(string='IP address')
    luxis_language = fields.Char(string='Language')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update({
            'luxis_status': params.get_param('sale_order_export_rpl.luxis_status', default=False),
            'luxis_payment_id': params.get_param('sale_order_export_rpl.luxis_payment_id', default="12"),
            'luxis_ip_address': params.get_param('sale_order_export_rpl.luxis_ip_address', default=False),
            'luxis_language': params.get_param('sale_order_export_rpl.luxis_language', default=False),
        })
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("sale_order_export_rpl.luxis_status", self.luxis_status)
        self.env['ir.config_parameter'].sudo().set_param("sale_order_export_rpl.luxis_payment_id", self.luxis_payment_id)
        self.env['ir.config_parameter'].sudo().set_param("sale_order_export_rpl.luxis_ip_address", self.luxis_ip_address)
        self.env['ir.config_parameter'].sudo().set_param("sale_order_export_rpl.luxis_language", self.luxis_language)
