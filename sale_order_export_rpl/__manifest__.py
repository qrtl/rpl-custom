# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Export Sale Order Data",
    "summary": "",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale_stock", "report_csv"],
    "data": ["report/sale_order_reports.xml", "views/res_config_settings_views.xml", "views/product_template_views.xml", "views/res_partner_views.xml", "views/sale_order_views.xml"],
}
