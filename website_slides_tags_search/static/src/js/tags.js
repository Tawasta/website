odoo.define('website_slides_tags_search.multiple_select', function (require) {
    "use strict";

    var _t = require('web.core')._t;

    $(function() {
        $('#tags_select').select2({
            placeholder: _t("Tags:"),
            allowClear: true,
        });

        $('#tags_select').on('change', function() {
            const newVal = $('#tags_select').val();
            if(newVal) {
                $('#tags_search').val(newVal);
            } else {
                $('#tags_search').val("");
            }
        });
    });
});

