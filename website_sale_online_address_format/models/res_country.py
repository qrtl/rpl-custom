# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re

from odoo import api, fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    online_address_format = fields.Text(
        string="Layout in Online Form",
        help="Display format to use for website address form belonging to this country.\n\n"  # noqa
        "You can use python-style string pattern with all the fields of the address "
        "(for example, use '%(street)s' to display the field 'street') plus"
        "\n%(state_name)s: the name of the state"
        "\n%(state_code)s: the code of the state"
        "\n%(country_name)s: the name of the country"
        "\n%(country_code)s: the code of the country",
    )

    @api.multi
    def get_online_address_fields(self):
        self.ensure_one()
        return re.findall(r"\((.+?)\)", self.online_address_format)
