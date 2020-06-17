# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Export Sale Order Data",
    "summary": "",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_stock", "sale_comment_template_ext", "report_csv", "delivery"],
    "data": [
        "data/ir_actions_data.xml",
        "report/sale_order_reports.xml",
        "views/res_config_settings_views.xml",
        "views/product_product_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
}
