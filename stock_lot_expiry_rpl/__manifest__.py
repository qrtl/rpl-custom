# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Lot Expiry RPL',
    'version': '12.0.1.0.0',
    'author': 'Quartile Limited',
    'website': 'https://www.quartile.co',
    'category': 'Stock',
    'license': "AGPL-3",
    'description': """
- Adds special logic to calculates removal_date of lots (and quants).
    """,
    'depends': [
        'product_expiry',
        'stock_quant_list_view',
    ],
    'data': [
        'views/product_template_views.xml',
        'views/stock_quant_views.xml',
    ],
    'installable': True,
}
