# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Sale Increase Refrigerant",
    "version": "12.0.1.2.0",
    "category": "Website",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website_sale"],
    "data": [
        "views/report_picking.xml",
        "views/res_country_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/templates.xml",
    ],
}
