# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from io import StringIO

from odoo import models


class ReportCSVCustom(models.AbstractModel):
    _name = "report.report_csv.custom"
    _inherit = "report.report_csv.abstract"

    # Overriding the method from report_csv so that different 'quoting'
    # parameters can be set for header and body in generate_csv_report method.
    def create_csv_report(self, docids, data):
        objs = self._get_objs_for_report(docids, data)
        file_data = StringIO()
        self.generate_csv_report(data, objs, file_data)
        file_data.seek(0)
        return file_data.read(), "csv"
