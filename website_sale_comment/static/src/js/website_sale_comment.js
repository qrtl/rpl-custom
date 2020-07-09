odoo.define("website_sale_comment_tour_sale.tour_shop_customize", function(require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    tour.register(
        "website_sale_comment_tour_sale",
        {
            test: true,
            url: "/shop",
            wait_for: base.ready(),
        },
        [
            {
                content: "search conference chair",
                trigger: 'form input[name="search"]',
                run: "text conference chair",
            },
            {
                content: "search conference chair",
                trigger: 'form:has(input[name="search"]) .oe_search_button',
            },
            {
                content: "select conference chair",
                trigger: '.oe_product_cart:first a:contains("Conference Chair")',
            },
            {
                content: "select Conference Chair Aluminium",
                extra_trigger: "#product_detail",
                trigger: "label:contains(Aluminium) input",
            },
            {
                content: "select Conference Chair Steel",
                extra_trigger: "#product_detail",
                trigger: "label:contains(Steel) input",
            },
            {
                content: "click on add to cart",
                extra_trigger: "label:contains(Steel) input:propChecked",
                trigger:
                    '#product_detail form[action^="/shop/cart/update"] .btn-primary',
            },
            {
                content: "click in modal on 'Proceed to checkout' button",
                trigger: 'button:contains("Proceed to Checkout")',
            },
            {
                content: "add suggested",
                extra_trigger:
                    '#wrap:not(:has(#cart_products:contains("Storage Box")))',
                trigger:
                    '.oe_cart:has(tr:contains("Storage Box")) a:contains("Add to Cart")',
            },
            {
                content: "add one more",
                extra_trigger: '#cart_products tr:contains("Storage Box")',
                trigger: '#cart_products tr:contains("Steel") a.js_add_cart_json:eq(1)',
            },
            {
                content: "remove Storage Box",
                extra_trigger:
                    '#cart_products tr:contains("Steel") input.js_quantity:propValue(2)',
                trigger:
                    '#cart_products tr:contains("Storage Box") a.js_add_cart_json:first',
            },
            {
                content: "set one",
                extra_trigger:
                    '#wrap:not(:has(#cart_products tr:contains("Storage Box")))',
                trigger: "#cart_products input.js_quantity",
                run: "text 1",
            },

            {
                content: "open customize menu",
                trigger: "#customize-menu > a",
            },
            {
                content: "click on 'Product Attribute's Filters'",
                trigger: "#customize-menu a:contains(Extra Step Option)",
            },
            {
                content: "go to checkout",
                trigger: "a:contains(Process Checkout)",
                run: "click",
            },
            {
                trigger: "textarea[name='Give us your feedback']",
                run: "click",
            },
            {
                content: "Complete Feedback",
                trigger: "textarea[name='Give us your feedback']",
                run: "text Test Feedback Comment",
            },

            {
                trigger: ".o_website_form_send",
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
