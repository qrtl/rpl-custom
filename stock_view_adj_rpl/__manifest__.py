# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock View Adjustments",
    "version": "12.0.1.0.4",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "category": "Stock",
    "license": "AGPL-3",
    "depends": ["delivery", "stock_move_location"],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_production_lot_view.xml",
        "wizard/stock_move_location.xml",
    ],
    "installable": True,
}
