# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common


class TestStockLotExpiryRpl(common.TransactionCase):
    def setUp(self):
        # create products with date params
        super(TestStockLotExpiryRpl, self).setUp()
        self.productAAA = self.env["product.product"].create(
            {
                "name": "Product AAA",
                "type": "product",
                "tracking": "lot",
                "base_date": 1,
                "weekday_delta": -1,
                "month_delta": 12,
                "day_delta": -1,
            }
        )
        self.productBBB = self.env["product.product"].create(
            {
                "name": "Product AAA",
                "type": "product",
                "tracking": "lot",
                "base_date": 0,
                "weekday_delta": 0,
                "month_delta": 24,
                "day_delta": 0,
            }
        )
        self.productCCC = self.env["product.product"].create(
            {
                "name": "Product AAA",
                "type": "product",
                "tracking": "lot",
                "base_date": 1,
                "weekday_delta": 1,
                "month_delta": 12,
                "day_delta": -1,
            }
        )

    # '2019-06-01 08:00:00' JP - UTC and JP are in different months
    def test_00_stock_lot_expiry(self):
        date_utc = fields.Datetime.to_datetime("2019-05-31 23:00:00")
        date = (
            self.env["stock.production.lot"]
            .with_context({"tz": "Japan"})
            ._calculate_expiry_date(self.productAAA.id, date_utc)
        )
        self.assertEqual(date, "2020-05-25 23:00:00")

    # '2019-06-01 10:00:00' JP - UTC and JP are in the same month
    def test_01_stock_lot_expiry(self):
        date_utc = fields.Datetime.to_datetime("2019-06-01 01:00:00")
        date = (
            self.env["stock.production.lot"]
            .with_context({"tz": "Japan"})
            ._calculate_expiry_date(self.productAAA.id, date_utc)
        )
        self.assertEqual(date, "2020-05-26 01:00:00")

    # 1st of the month is Monday (weekday_delta is -1)
    def test_02_stock_lot_expiry(self):
        date_utc = fields.Datetime.to_datetime("2019-04-10 01:00:00")
        date = (
            self.env["stock.production.lot"]
            .with_context({"tz": "Japan"})
            ._calculate_expiry_date(self.productAAA.id, date_utc)
        )
        self.assertEqual(date, "2020-03-24 01:00:00")

    # 1st of the month is Monday (weekday_delta is +1)
    def test_03_stock_lot_expiry(self):
        date_utc = fields.Datetime.to_datetime("2019-04-10 01:00:00")
        date = (
            self.env["stock.production.lot"]
            .with_context({"tz": "Japan"})
            ._calculate_expiry_date(self.productCCC.id, date_utc)
        )
        self.assertEqual(date, "2020-04-07 01:00:00")

    # 24 months from 29 Feb
    def test_04_stock_lot_expiry(self):
        date_utc = fields.Datetime.to_datetime("2020-02-29 01:00:00")
        date = (
            self.env["stock.production.lot"]
            .with_context({"tz": "Japan"})
            ._calculate_expiry_date(self.productBBB.id, date_utc)
        )
        self.assertEqual(date, "2022-02-28 01:00:00")
