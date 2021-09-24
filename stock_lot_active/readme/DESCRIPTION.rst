This module does the following:

* Adds the active field to stock.production.lot to enable archiving function for
  lot/serials.

Archiving is prevented when the lot/serial has the history of product moves (i.e.
quants are linked to it).
