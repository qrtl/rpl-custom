# Copyright 2019 Quartile Limited
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
    "description": """
    Add 'Country Groups' to 'Product Attributes Value', filter out the
    products options on e-commerce if the country of the user is not in the
    set 'Country Groups'.
    """,
    "depends": ["website_sale",],
    "data": [
        "views/product_attribute_value_views.xml",
        "views/sale_product_configurator_templates.xml",
    ],
}
