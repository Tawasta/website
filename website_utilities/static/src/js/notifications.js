odoo.define("website_utilities.notifications", function () {
    "use strict";

    $(function () {

        // Toastr -jQuery plugin used for notifications
        toastr.options = {
            "positionClass": "toast-bottom-center",
            "closeButton": true,
            "debug": false,
            "preventDuplicates": true,
            "onclick": null,
            "showDuration": "100",
            "hideDuration": "1000",
            "timeOut": "3000",
            "extendedTimeOut": "1000",
            "tapToDismiss": false,
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut",
        };
    });

    return {
        toastr: toastr,
    };
});
