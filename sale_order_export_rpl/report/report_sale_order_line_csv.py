# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
from io import StringIO

from odoo import models


class SaleOrderLineCSV(models.AbstractModel):
    _name = "report.report_csv.sale_order_line_csv"
    _inherit = "report.report_csv.abstract"

    def create_csv_report(self, docids, data):
        objs = self._get_objs_for_report(docids, data)
        file_data = StringIO()
        self.generate_csv_report(data, objs, file_data)
        file_data.seek(0)
        return file_data.read(), "csv"

    def generate_csv_report(self, data, orders, file_data):
        writer = csv.DictWriter(
            file_data, **self.csv_report_options(), quoting=csv.QUOTE_NONE
        )
        writer.writeheader()
        writer = csv.DictWriter(
            file_data, **self.csv_report_options(), quoting=csv.QUOTE_ALL
        )
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
                            "Quantity": int(line.product_uom_qty),
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
        res["lineterminator"] = "\n"
        return res
