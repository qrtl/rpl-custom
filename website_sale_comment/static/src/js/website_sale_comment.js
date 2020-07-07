odoo.define('website_sale_comment.tour', function (require) {
    'use strict';

    var tour = require('web_tour.tour');
    var base = require('web_editor.base');

    tour.register('website_sale_comment_tour', {
        test: true,
        url: '/shop/cart',
        wait_for: base.ready(),
    }, [

        {
            content: "open customize menu",
            trigger: '#customize-menu > .dropdown-toggle',
        },
        {
            content: "check the selection",
            trigger: 'form.js_attributes label:contains(Extra Step Option) input:checked',
            run: function () {}, // it's a check
        },
        // {
        //     content: "Checked Extra Step Option",
        //     trigger: "#customize-menu a:contains(Extra Step Option)input:checked",
        //     run: function () {
        //     }
        //
        // },
        // {
        //     content: "Checked Extra Step Option",
        //     trigger: '#customize-menu > a:contains("Extra Step Option"):has(input:checked)',
        //     run: function () {
        //     }
        // },
        {
            content: "click in modal on 'Proceed to checkout' button",
            trigger: 'a:contains("Process Checkout")',
        },
        {
            trigger: "textarea[name='Give us your feedback']",
            run: "click",
        },
        //
        {
            content: "Complete Feedback",
            trigger: "textarea[name='Give us your feedback']",
            run: "text Test Feedback Comment"
        },
        {
            trigger: ".o_website_form_send",
            run: "click"
        },
        {
            content: "select payment",
            trigger: '#payment_method label:contains("Wire Transfer")',
        },
        {
            content: "Pay Now",
            //Either there are multiple payment methods, and one is checked, either there is only one, and therefore there are no radio inputs
            extra_trigger: '#payment_method label:contains("Wire Transfer") input:checked,#payment_method:not(:has("input:radio:visible"))',
            trigger: 'button[id="o_payment_form_pay"]:visible:not(:disabled)',
        }

    ]);
});
