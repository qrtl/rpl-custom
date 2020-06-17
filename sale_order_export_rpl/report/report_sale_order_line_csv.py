# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv

from odoo import models


class SaleOrderLineCSV(models.AbstractModel):
    _name = "report.report_csv.sale_order_line_csv"
    _inherit = "report.report_csv.abstract"

    def generate_csv_report(self, writer, data, orders):
        writer.writeheader()
        for order in orders:
            for line in order.order_line:
                if not line.is_delivery:
                    writer.writerow(
                        {
                            "Order ID": order.rakushisu_order_id,
                            "Item ID": line.product_id.rakushisu_item_id or "",
                            "Product ID": line.product_id.rakushisu_product_id or "",
                            "Product code": "",
                            "Price": line.price_unit,
                            "Quantity": line.product_uom_qty,
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
