odoo.define('website_utilities.loader', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;


    var loadingScreen = function () {
        // Block UI when adding a new vocational unit to student
        var translate_message = _t("Loading, please wait...");
        var display_message = '<img src="/web/static/src/img/spin.png"\
            style="animation: fa-spin 1s infinite steps(12);"/>\
            <br/><br/><h4>' + translate_message +'</h4>';

        // Loading screen
        $.blockUI({
            message: display_message,
            css: {
                padding: 0,
                margin: 0,
                width: '30%',
                top: '40%',
                left: '35%',
                textAlign: 'center',
                cursor: 'wait',
                backgroundColor: 'transparent',
                color: '#fff',
                border: 0,
            },
        });
    };

    $(function () {
        // Unblock when page has reloaded
        $.unblockUI();
    });

    $(window).on("pageshow", function () {
        $.unblockUI();
    });

    return {
        loadingScreen: loadingScreen,
    };
});
