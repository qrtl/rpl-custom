# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Sale Comment",
    "summary": "Allows to leave a message when checkouting an order from website",
    "version": "12.0.1.2.1",
    "category": "Website",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website_sale", "sale_comment_template"],
    "data": ["views/templates.xml", "views/website_sale_template.xml"],
}
