odoo.define('website_unread_messages.unread_messages', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var toastr = require('website_utilities.notifications').toastr;

    // Upon page reload, check for new messages
    function checkNewMessages() {
        var action = '/new_messages/';
        var msg = "";

        ajax.jsonRpc(action, "call").then(function (res) {
            var response = JSON.parse(res);
            var is_enabled = response['is_enabled']
            var notification = response['notification_class'];
            if (is_enabled && notification == 'info' && response['msg'] != "") {
                toastr.info(response['msg']);
            } else if (is_enabled && notification == 'success' && response['msg'] != "") {
                toastr.success(response['msg']);
            }
        });
    }

    $(function () {
        checkNewMessages();      
    });
});
