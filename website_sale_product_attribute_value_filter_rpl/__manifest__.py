# Copyright 2019-2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Attribute Value Filter RPL",
    "summary": "",
    "version": "12.0.1.0.0",
    "category": "Website",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_attribute_value_permission_views.xml",
        # "views/product_attribute_value_views.xml",
        "views/sale_product_configurator_templates.xml",
    ],
}
