This module does the following:

* Adds the component lot filter field to the manufacturing order, and checks
  the consistency between the filter value and the selected lots for the
  component products that have been indicated for checking.
* Disallow reservation of more than one lot per component line.
* Suggests the maximum producible quantity according to the lots selected for
  the component lines.
