This module does the following:

* Extends the standard method that computes the available acquirers in the eCommerce
  checkout, to apply the following logic:

  * If there is an acquirer which is linked to the partner (sold-to), only show that
    acquirer.
  * Otherwise, show the acquirers (except for the special ones linked to partners)
    following the standard logic.
