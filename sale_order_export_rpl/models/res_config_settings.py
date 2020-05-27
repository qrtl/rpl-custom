# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    rakushisu_status = fields.Char(string="Status")
    rakushisu_payment_id = fields.Char(string="Payment ID")
    rakushisu_ip_address = fields.Char(string="IP address")
    rakushisu_language = fields.Char(string="Language")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            {
                "rakushisu_status": params.get_param(
                    "sale_order_export_rpl.rakushisu_status", default=False
                ),
                "rakushisu_payment_id": params.get_param(
                    "sale_order_export_rpl.rakushisu_payment_id", default="12"
                ),
                "rakushisu_ip_address": params.get_param(
                    "sale_order_export_rpl.rakushisu_ip_address", default=False
                ),
                "rakushisu_language": params.get_param(
                    "sale_order_export_rpl.rakushisu_language", default=False
                ),
            }
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "sale_order_export_rpl.rakushisu_status", self.rakushisu_status
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "sale_order_export_rpl.rakushisu_payment_id", self.rakushisu_payment_id
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "sale_order_export_rpl.rakushisu_ip_address", self.rakushisu_ip_address
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "sale_order_export_rpl.rakushisu_language", self.rakushisu_language
        )
