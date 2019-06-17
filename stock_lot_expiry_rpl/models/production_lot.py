# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    def _get_dates(self, product_id=None):
        res = super(StockProductionLot, self)._get_dates(product_id)
        removal_date = self._calculate_expiry_date(product_id)
        if removal_date:
            res['removal_date'] = removal_date
        return res

    def _calculate_expiry_date(self, product_id=None, date=datetime.now()):
        p = self.env['product.product'].browse(product_id) or self.product_id
        if p and p.base_date or p.month_delta or p.weekday_delta or \
                p.day_delta:
            # temporarily convert date according to user's timezone for
            # relativedelta operations
            date = fields.Datetime.context_timestamp(self, date)
            date += relativedelta(day=p.base_date)
            if p.weekday_delta:
                # we need to have this step in case date falls into Monday -
                # see "e.g. if the calculated date is already Monday, using
                # MO(1) or MO(-1) won't change the day" from
                # https://dateutil.readthedocs.io/en/stable/relativedelta.html
                adjusted_delta = (abs(p.weekday_delta)+1) * \
                    (abs(p.weekday_delta)/p.weekday_delta)
                weekday_delta = adjusted_delta if date.weekday() == 0 else p.weekday_delta
                date += relativedelta(weekday=MO(weekday_delta))
            date += relativedelta(months=p.month_delta)
            date += relativedelta(days=p.day_delta)
            # convert date back to utc
            date = date.astimezone(pytz.utc)
            return fields.Datetime.to_string(date)
        return False
