# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Sales Order Increase Refrigerant",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale_stock"],
    "data": [
        "views/report_picking.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
}
