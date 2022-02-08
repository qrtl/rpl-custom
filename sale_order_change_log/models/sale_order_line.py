# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.order_id._message_log(
            body=_("Added: %s, %s") % (res.product_id.display_name, res.product_uom_qty)
        )
        return res

    @api.multi
    def unlink(self):
        self.order_id._message_log(
            body=_("Deleted: %s, %s")
            % (self.product_id.display_name, self.product_uom_qty)
        )
        return super().unlink()

    @api.multi
    def write(self, vals):
        if not vals.get("product_id") and "product_uom_qty" not in vals:
            return super().write(vals)
        for line in self:
            self._cr.execute(
                """
                SELECT
                    product_id, product_uom_qty
                FROM
                    sale_order_line
                WHERE id = %s
            """,
                (line.id,),
            )
            query_res = self._cr.dictfetchone()
            if not query_res:
                continue
            prev_product_id = query_res["product_id"]
            prev_qty = query_res["product_uom_qty"]
            prev_product = self.env["product.product"].browse(prev_product_id)
            if vals.get("product_id") and prev_product_id != vals.get("product_id"):
                new_product = self.env["product.product"].browse(vals.get("product_id"))
            else:
                new_product = prev_product
            if "product_uom_qty" in vals:
                # '0.0 +' is here just so the qty presentation gets consistent with
                # what's from the model field. i.e. without this, the new qty
                # presentation becomes '5' where we would like to show '5.0'.
                new_qty = 0.0 + vals.get("product_uom_qty")
            else:
                new_qty = prev_qty
            self.order_id._message_log(
                body=_("Changed: %s, %s → %s, %s")
                % (
                    prev_product.display_name,
                    prev_qty,
                    new_product.display_name,
                    new_qty,
                )
            )
        return super().write(vals)
