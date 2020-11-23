odoo.define("website_sale_change_payment_fee.website_sale_fee", function(require) {
    "use strict";

    require("web.dom_ready");
    require("web.ajax");
    require("web.core");

    $(".o_payment_form").each(function() {
        var selected_acquirer = $('input[name="pm_id"][checked="True"]')[0].value;

        $(this).on("click", 'input[name="pm_id"]', function() {
            var clicked_acquirer = $(this).prop("value");
            // Check whether saved token / payment method is being selected.
            if (clicked_acquirer.includes("_") === true) {
                // Represents the form id, e.g. form_5
                var acquirer_id = clicked_acquirer.split("_")[1];
                var checked_pm_id = "";
            } else {
                // Search the acquirer from the saved token, data-provider='stripe'
                var acquirer_id = $(
                    "input[data-provider=" + $(this).attr("data-provider") + "]"
                )[0].value.split("_")[1];
                var checked_pm_id = $(this).val();
            }
            if (selected_acquirer !== clicked_acquirer) {
                // Follow standard logic disabling the "Pay Now" button
                // https://github.com/odoo/odoo/blob/c2cce50f75096fcc9f940d16bb0ecf40a2899d60/addons/website_sale_delivery/static/src/js/website_sale_delivery.js#L56
                $("#o_payment_form_pay").prop("disabled", true);
                window.location.href =
                    "/shop/payment?payment_fee_id=" +
                    acquirer_id +
                    "&pm_id=" +
                    checked_pm_id;
            }
        });
    });
});
