# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Report Common Py3o',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'license': 'AGPL-3',
    'description': """
This module adds common fields that are used in py3o reports.
    """,
    'author': 'Quartile Limited',
    'depends': [
        'base',
        'report_py3o',
    ],
    'data': [
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
