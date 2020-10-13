# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Link Purchase Order to Subcontract Productions",
    "version": "12.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "depends": ["purchase", "mrp_subcontracting"],
    "data": ["views/purchase_order_views.xml", "views/mrp_production_views.xml"],
    "installable": True,
}
