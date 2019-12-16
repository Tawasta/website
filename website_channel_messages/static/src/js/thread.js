odoo.define("website_channel_messages.thread", function (require) {
    "use strict";

    var core = require("web.core");
    var ajax = require("web.ajax");
    var _t = core._t;
    var toastr = require("website_utilities.notifications").toastr;

    require("web.dom_ready");

    // Update message thread
    function updateMessages () {
        var record = $("#maincontent").attr("data-record-id");
        var route = "/website_channel/update_messages";
        var timestamp = $("#maincontent").attr("data-timestamp");
        var payload = {
            channel_id: parseInt(record) || 0,
            timestamp: timestamp,
            csrf_token: core.csrf_token,
        };
        var msg = "";
        if (document.hasFocus()) {
            ajax.jsonRpc(route, "call", payload).then(function (res) {
                if (res !== "") {
                    var new_date = (new Date().getTime() / 1000);
                    $("#maincontent").attr("data-timestamp", new_date);
                    var cleaned = res.replace("data-src", "src");
                    $("#channel_messages").prepend(cleaned);
                    msg = _t("New message arrived!");
                    toastr.info(msg);
                }
            });
        }
    }

    var record = $("#maincontent").attr("data-record-id");

    if (record !== undefined) {
        $(window).scroll(function() {
            $(".msg-img").each(function(i) {
                var bottom_of_object = $(this).offset().top + $(this).outerHeight();
                var bottom_of_window = $(window).scrollTop() + $(window).height();
                if (bottom_of_window > bottom_of_object &&
                        $(this).attr("src") == undefined) {
                    $(this).attr("src", $(this).attr("data-src"));
                }
            });
        });
        setTimeout(function () {
            $(window).scroll();
        }, 100);

        setInterval(function () {
            updateMessages();
        }, $("#channel_messages").attr("data-interval"));
    }
});
