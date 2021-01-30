# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "MRP Production Component Lot Constraint",
    "version": "12.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["mrp_production_quant_manual_assign"],
    "data": [
        "views/mrp_production_views.xml",
        "views/product_template_views.xml",
    ],
}
