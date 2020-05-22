# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import csv

from odoo import models


class SaleOrderLineCSV(models.AbstractModel):
    _name = "report.report_csv.sale_order_line_csv"
    _inherit = "report.report_csv.abstract"

    def generate_csv_report(self, writer, data, orders):
        writer.writeheader()
        for order in orders:
            for order_line in order.order_line:
                writer.writerow(
                    {
                        "Order ID": order.luxis_order_id,
                        "Item ID": order_line.product_id.luxis_item_id or "",
                        "Product ID": order_line.product_id.luxis_product_id or "",
                        "Product code": "",
                        "Price": order_line.price_unit,
                        "Quantity": order_line.product_uom_qty,
                        "Extra": "",
                    }
                )

    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("Order ID")
        res["fieldnames"].append("Item ID")
        res["fieldnames"].append("Product ID")
        res["fieldnames"].append("Product code")
        res["fieldnames"].append("Price")
        res["fieldnames"].append("Quantity")
        res["fieldnames"].append("Extra")
        res["delimiter"] = ","
        res["quoting"] = csv.QUOTE_ALL
        return res
