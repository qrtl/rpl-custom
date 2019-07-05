# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import request
from odoo import models


class Website(models.Model):
    _inherit = 'website'

    def get_partner_country_info(self):
        if request.env.user.partner_id.country_id:
            return request.env.user.partner_id.country_id.code,\
                str(request.env.user.partner_id.country_id.id)
        return False
