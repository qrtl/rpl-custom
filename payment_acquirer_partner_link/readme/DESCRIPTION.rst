This module does the following:

* Adds partner field to the payment acquirer model (many2many) which is supposed to be
  used for direct debit payment.
* Adds the acquirer field in account.invoice, and proposes a value based on the
  following logic:

  * If there is a payment transaction attached to the invoice, take the acquirer from
    the payment transaction.
  * Otherwise, take the acquirer from the commercial partner of the invoice.

The background
--------------

The direct debit payment method is exclusive to certain customers and should not be
made publicly available.
