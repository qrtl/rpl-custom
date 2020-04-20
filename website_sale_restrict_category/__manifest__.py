# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Sale Restrict Category",
    "category": "Website",
    "version": "12.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co/",
    "license": "LGPL-3",
    "depends": ["website_sale"],
    "data": [
        "security/security.xml",
        "views/product_public_category_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
