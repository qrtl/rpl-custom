odoo.define("website_sale_disable_express_checkout.tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    tour.register(
        "website_sale_disable_express_checkout",
        {
            test: true,
            url: "/shop/cart",
            wait_for: base.ready(),
        },
        [
            {
                content: "click in modal on 'Proceed to checkout' button",
                trigger: 'a:contains("Process Checkout")',
            },
            {
                trigger: 'a:contains("Confirm")',
                run: "click",
            },
            {
                content: "select payment",
                trigger: '#payment_method label:contains("Wire Transfer")',
            },
            {
                content: "Pay Now",
                // Either there are multiple payment methods, and one is checked, either there is only one, and therefore there are no radio inputs
                extra_trigger:
                    '#payment_method label:contains("Wire Transfer") input:checked,#payment_method:not(:has("input:radio:visible"))',
                trigger: 'button[id="o_payment_form_pay"]:visible:not(:disabled)',
            },
        ]
    );
});
