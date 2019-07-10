odoo.define('website_unread_messages.mark_read', function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var session = require('web.session');

    $(function () {

        // var MessageModel = new Model('mail.message', session.user_context);
        $('.read-confirm').on('click', function() {
            // MessageModel.call('mark_all_as_read', []).then(function() {
                
            // });
            rpc.query({
                model: 'mail.message',
                method: 'mark_all_as_read',
            }).then(function(res) {
                console.log(res);
                // location.reload();
            });
        });
    });
});
