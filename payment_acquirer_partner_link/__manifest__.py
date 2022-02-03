# Copyright 2021 -2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Payment Acquirer Partner Link",
    "version": "12.0.1.0.0",
    "category": "Accounting",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["payment"],
    "data": [
        "views/account_invoice_views.xml",
        "views/payment_acquirer_views.xml",
        "views/res_partner_views.xml",
    ],
}
