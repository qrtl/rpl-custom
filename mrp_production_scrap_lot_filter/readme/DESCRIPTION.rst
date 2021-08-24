This module does the following:

* Calculates the lot values to pass to the domain filter on the lot field in of the
  scrap form that is called from the production form.

  * For ongoing productions, only the lots that are assigned for the component lines
    can be selected.
  * For completed productions, only the lot that was created in the production can be
    selected.

This module depends on stock_picking_scrap_lot_filter.
