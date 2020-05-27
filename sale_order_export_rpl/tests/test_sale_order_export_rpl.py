# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
from io import StringIO

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderExportRPL(common.TransactionCase):
    def setUp(self):
        super().setUp()
        report_object = self.env["ir.actions.report"]
        self.csv_report = self.env["report.report_csv.abstract"].with_context(
            active_model="sale.order"
        )
        self.order_report_name = "report_csv.sale_order_csv"
        self.order_line_report_name = "report_csv.sale_order_line_csv"
        self.order_report = report_object._get_report_from_name(self.order_report_name)
        self.order_line_report = report_object._get_report_from_name(
            self.order_line_report_name
        )
        self.docs = self.env["sale.order"].search([], limit=1)

    def test_order_report(self):
        report = self.order_report
        self.assertEqual(report.report_type, "csv")
        rep = report.render(self.docs.ids, {})
        str_io = StringIO(rep[0])
        dict_report = list(csv.DictReader(str_io, delimiter=",", quoting=csv.QUOTE_ALL))
        self.assertEqual(self.docs.rakushisu_order_id, dict(dict_report[0])["Order ID"])
        self.assertEqual(self.docs.partner_id.email, dict(dict_report[0])["E-mail"])
        self.assertEqual(
            self.docs.partner_id.rakushisu_user_id or "", dict(dict_report[0])["User ID"]
        )
        self.assertEqual(str(self.docs.amount_total), dict(dict_report[0])["Total"])
        self.assertEqual(
            str(self.docs.amount_total - self.docs.delivery_price),
            dict(dict_report[0])["Subtotal"],
        )
        self.assertEqual("0", dict(dict_report[0])["Discount"])
        self.assertEqual("0", dict(dict_report[0])["Payment surcharge"])
        self.assertEqual(
            str(self.docs.delivery_price), dict(dict_report[0])["Shipping cost"]
        )
        self.assertEqual(
            self.docs.confirmation_date
            and self.docs.confirmation_date.strftime("%d/%m/%Y %H:%M")
            or "",
            dict(dict_report[0])["Date"],
        )
        self.assertEqual(
            self.docs.rakushisu_status
            or self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_export_rpl.rakushisu_status", default=""),
            dict(dict_report[0])["Status"],
        )
        self.assertEqual(self.docs.note, dict(dict_report[0])["Notes"])
        self.assertEqual(
            str(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("sale_order_export_rpl.rakushisu_payment_id", default=12)
            ),
            dict(dict_report[0])["Payment ID"],
        )
        self.assertEqual(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_export_rpl.rakushisu_ip_address", default=""),
            dict(dict_report[0])["IP address"],
        )
        self.assertEqual(self.docs.note2 or "", dict(dict_report[0])["Details"])
        self.assertEqual("", dict(dict_report[0])["Payment information"])
        self.assertEqual("", dict(dict_report[0])["Taxes"])
        self.assertEqual("", dict(dict_report[0])["Coupons"])
        self.assertEqual("", dict(dict_report[0])["Shipping"])
        self.assertEqual("", dict(dict_report[0])["Title"])
        self.assertEqual("", dict(dict_report[0])["First name"])
        self.assertEqual("", dict(dict_report[0])["Last name"])
        self.assertEqual(
            self.docs.partner_id.parent_id
            and self.docs.user_id.partner_id.parent_id.name
            or "",
            dict(dict_report[0])["Company"],
        )
        self.assertEqual("", dict(dict_report[0])["Fax"])
        self.assertEqual(
            self.docs.partner_shipping_id.phone, dict(dict_report[0])["Phone"]
        )
        self.assertEqual("", dict(dict_report[0])["Web site"])
        self.assertEqual("N", dict(dict_report[0])["Tax exempt"])
        self.assertEqual(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_export_rpl.rakushisu_language", default=""),
            dict(dict_report[0])["Language"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.title
            and self.docs.partner_invoice_id.title.name
            or "",
            dict(dict_report[0])["Billing: title"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.name,
            dict(dict_report[0])["Billing: first name"],
        )
        self.assertEqual("", dict(dict_report[0])["Billing: last name"])
        self.assertEqual(
            self.docs.partner_invoice_id.street or "",
            dict(dict_report[0])["Billing: address"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.street2 or "",
            dict(dict_report[0])["Billing: address (line 2)"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.city or "",
            dict(dict_report[0])["Billing: city"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.state_id
            and self.docs.partner_invoice_id.state_id.code
            or "",
            dict(dict_report[0])["Billing: state"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.country_id
            and self.docs.partner_invoice_id.country_id.code
            or "",
            dict(dict_report[0])["Billing: country"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.zip, dict(dict_report[0])["Billing: zipcode"]
        )
        self.assertEqual(
            self.docs.partner_shipping_id.title
            and self.docs.partner_shipping_id.title.name
            or "",
            dict(dict_report[0])["Shipping: title"],
        )
        self.assertEqual(
            self.docs.partner_shipping_id.name,
            dict(dict_report[0])["Shipping: first name"],
        )
        self.assertEqual("", dict(dict_report[0])["Shipping: last name"])
        self.assertEqual(
            self.docs.partner_shipping_id.street or "",
            dict(dict_report[0])["Shipping: address"],
        )
        self.assertEqual(
            self.docs.partner_shipping_id.street2 or "",
            dict(dict_report[0])["Shipping: address (line 2)"],
        )
        self.assertEqual(
            self.docs.partner_shipping_id.city or "",
            dict(dict_report[0])["Shipping: city"],
        )
        self.assertEqual(
            self.docs.partner_shipping_id.state_id
            and self.docs.partner_shipping_id.state_id.code
            or "",
            dict(dict_report[0])["Shipping: state"],
        )
        self.assertEqual(
            self.docs.partner_shipping_id.country_id
            and self.docs.partner_shipping_id.country_id.code
            or "",
            dict(dict_report[0])["Shipping: country"],
        )
        self.assertEqual(
            self.docs.partner_invoice_id.zip, dict(dict_report[0])["Shipping: zipcode"]
        )
        self.assertEqual("", dict(dict_report[0])["Invoice ID"])
        self.assertEqual("", dict(dict_report[0])["Credit memo ID"])
        self.assertEqual("", dict(dict_report[0])["payment_date"])

    def test_order_line_report(self):
        report = self.order_line_report
        self.assertEqual(report.report_type, "csv")
        rep = report.render(self.docs.ids, {})
        str_io = StringIO(rep[0])
        dict_report = list(csv.DictReader(str_io, delimiter=",", quoting=csv.QUOTE_ALL))
        self.assertEqual(self.docs.rakushisu_order_id, dict(dict_report[0])["Order ID"])
        self.assertEqual(
            self.docs.order_line[0].product_id.rakushisu_item_id or "",
            dict(dict_report[0])["Item ID"],
        )
        self.assertEqual(
            self.docs.order_line[0].product_id.rakushisu_product_id or "",
            dict(dict_report[0])["Product ID"],
        )
        self.assertEqual("", dict(dict_report[0])["Product code"])
        self.assertEqual(
            str(self.docs.order_line[0].price_unit), dict(dict_report[0])["Price"]
        )
        self.assertEqual(
            str(self.docs.order_line[0].product_uom_qty),
            dict(dict_report[0])["Quantity"],
        )
        self.assertEqual("", dict(dict_report[0])["Extra"])

    def test_order_export_id_retrieval(self):
        # Typical call from WebUI with wizard
        objs = self.csv_report._get_objs_for_report(
            False, {"context": {"active_ids": self.docs.ids}}
        )
        self.assertEquals(objs, self.docs)
        # Typical call from within code not to report_action
        objs = self.csv_report.with_context(
            active_ids=self.docs.ids
        )._get_objs_for_report(False, False)
        self.assertEquals(objs, self.docs)
        # Typical call from WebUI
        objs = self.csv_report._get_objs_for_report(
            self.docs.ids,
            {"data": [self.order_report_name, self.order_report.report_type]},
        )
        self.assertEquals(objs, self.docs)
        # Typical call from render
        objs = self.csv_report._get_objs_for_report(self.docs.ids, {})
        self.assertEquals(objs, self.docs)

    def test_order_line_export_id_retrieval(self):
        # Typical call from WebUI with wizard
        objs = self.csv_report._get_objs_for_report(
            False, {"context": {"active_ids": self.docs.ids}}
        )
        self.assertEquals(objs, self.docs)
        # Typical call from within code not to report_action
        objs = self.csv_report.with_context(
            active_ids=self.docs.ids
        )._get_objs_for_report(False, False)
        self.assertEquals(objs, self.docs)
        # Typical call from WebUI
        objs = self.csv_report._get_objs_for_report(
            self.docs.ids,
            {"data": [self.order_line_report_name, self.order_line_report.report_type]},
        )
        self.assertEquals(objs, self.docs)
        # Typical call from render
        objs = self.csv_report._get_objs_for_report(self.docs.ids, {})
        self.assertEquals(objs, self.docs)
