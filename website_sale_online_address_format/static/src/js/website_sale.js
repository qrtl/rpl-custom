odoo.define("website_sale_online_address_format.website_sale", function(require) {
    "use strict";

    var sAnimations = require("website.content.snippets.animation");

    sAnimations.registry.WebsiteSale.include({
        /**
         * @private
         */
        // QRTL Edit: Overwrite _changeCountry() method from website_sale
        _changeCountry: function() {
            if (!$("#country_id").val()) {
                return;
            }
            this._rpc({
                route: "/shop/country_infos/" + $("#country_id").val(),
                params: {
                    mode: "shipping",
                },
            }).then(function(data) {
                // Placeholder phone_code
                // $("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                var selectStates = $("select[name='state_id']");
                // Dont reload state at first loading (done in qweb)
                if (
                    selectStates.data("init") === 0 ||
                    selectStates.find("option").length === 1
                ) {
                    if (data.states.length) {
                        selectStates.html("");
                        _.each(data.states, function(x) {
                            var opt = $("<option>")
                                .text(x[1])
                                .attr("value", x[0])
                                .attr("data-code", x[2]);
                            selectStates.append(opt);
                        });
                        selectStates.parent("div").show();
                    } else {
                        selectStates
                            .val("")
                            .parent("div")
                            .hide();
                    }
                    selectStates.data("init", 0);
                } else {
                    selectStates.data("init", 0);
                }

                // Manage fields order / visibility
                if (data.fields) {
                    // If ($.inArray('zip', data.fields) > $.inArray('city', data.fields)){
                    //     $(".div_zip").before($(".div_city"));
                    // } else {
                    //     $(".div_zip").after($(".div_city"));
                    // }
                    // QRTL Edit: Sort the fields according online_address_format
                    var previous_field = $(".div_street");
                    _.each(data.fields, function(field) {
                        previous_field.after($(".div_" + field.split("_")[0]));
                        previous_field = $(".div_" + field.split("_")[0]);
                    });
                    // Var all_fields = ["street", "zip", "city", "country_name"]; // "state_code"];
                    // QRTL Edit: Add street2 and state_code to all fields
                    var all_fields = [
                        "street",
                        "street2",
                        "zip",
                        "city",
                        "country_name",
                        "state_code",
                    ];
                    _.each(all_fields, function(field) {
                        $(".checkout_autoformat .div_" + field.split("_")[0]).toggle(
                            $.inArray(field, data.fields) >= 0
                        );
                    });
                }
            });
        },
    });
});
