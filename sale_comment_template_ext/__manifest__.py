# Copyright 2019-2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Sale Comments Ext",
    "summary": "Passes note field values to picking",
    "version": "12.0.1.1.0",
    "category": "Sale",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "data": ["views/report_saleorder.xml", "views/sale_order_views.xml"],
    "depends": ["sale_comment_template", "stock_picking_comment_template"],
}
