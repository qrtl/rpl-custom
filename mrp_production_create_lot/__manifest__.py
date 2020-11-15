# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "MRP Production Create Lot",
    "version": "12.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["mrp", "stock_lot_management_rpl"],
    "data": [
        "views/mrp_production_views.xml",
    ]
}
