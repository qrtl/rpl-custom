# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Generate QR Code for Lot",
    "version": "12.0.1.0.0",
    "author": "Quartile Limited",
    "category": "Warehouse",
    "website": "https://www.quartile.co",
    "summary": "QR code for Lot",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "data/stock_serial_data.xml",
        "security/ir.model.access.csv",
        "views/stock_serial_views.xml",
        "views/stock_production_lot_views.xml",
    ],
    "application": False,
}
