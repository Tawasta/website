odoo.define("website_unread_messages.mark_read", function (require) {
    "use strict";

    var rpc = require("web.rpc");

    $(function () {

        $(".read-confirm").on("click", function () {
            rpc.query({
                model: "mail.message",
                method: "mark_all_as_read",
            }).then(function() {
                location.reload();
            });
        });
    });
});
