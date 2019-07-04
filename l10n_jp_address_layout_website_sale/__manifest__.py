# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Japan Address Layout in E-commerce and website',
    'version': '12.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'category': 'Extra Tools',
    'license': "AGPL-3",
    'description': """
This module provides the Japan address input field layout in E-commerce.

If you have any inquiries, please free feel to contact us via info@quartile.co 
    """,
    'summary': "",
    'depends': [
        'portal',
        'website_sale',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
}
