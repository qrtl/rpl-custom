# Copyright 2019-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Comments Ext",
    "summary": "Passes note field values to picking",
    "version": "12.0.1.1.0",
    "category": "Sale",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "data": ["views/report_saleorder.xml", "views/sale_order_views.xml"],
    "depends": ["sale_comment_template", "stock_picking_comment_template"],
}
