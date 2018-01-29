# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2017 Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################


# 1. Standard library imports:
from datetime import datetime
import json
import time

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import _, http
from odoo.http import request

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in


class WebsiteUtilitiesController(http.Controller):

    @http.route(
        ['/new_messages/'],
        type='json',
        auth='user',
        website=True,
        csrf=False,
    )
    def new_messages(self, **post):
        """
        Route to return info about how many new messages partner has in
        the appointments.
        
        Use cases:
            Hide "No new messages" if the message has been displayed once
            Show message if state changes
            60 second cooldown, if the message is not marked as read

        Returns:
            -1 if no messages and message doesn't have to be displayed
            0 if no messages and message WILL BE displayed
            > 0 if new messages
        """
        current_user = http.request.env.user
        partner = current_user.partner_id
        timestamp = request.session.get('messages_checked')
        no_messages = _("There aren't any new messages!")
        msg = ""

        # Skills uses the regular needaction_count and vets uses the appointment one
        if current_user.has_group('medical.group_medical_user'):
            message_count, appointment_id = partner.sudo(current_user).get_appointment_needaction_count()
        else:
            message_count = partner.sudo(current_user).get_needaction_count()

        if timestamp:
            # Last new messages retrieved at timestamp
            timestamp_date = datetime.fromtimestamp(timestamp)
            difference = (datetime.now() - timestamp_date).seconds
            too_soon = True if difference < 60 else False

            if too_soon and message_count != 0:
                # Do not display message if message was displayed in the last
                # 60 seconds
                return False
            elif message_count == 0:
                # State changed to 'all messages are read' -> Display message
                request.session['messages_checked'] = None
        else:
            if message_count == 0:
                # No timestamp == no messages last time function was called
                return False

        if message_count != 0:
            # Save timestamp to prevent spam
            request.session['messages_checked'] = time.time()
            msg = _("You have ")

            if message_count > 1:
                msg += _("%d new messages in discussions!") % message_count
            else:
                msg += _("a new message in discussions!")
                
                # Add link to the discussion
                if current_user.has_group('medical.group_medical_user'):
                    discussion_href = '/medical/discussion/%s' % appointment_id
                    msg = "<a href='%s'>%s</a>" % (discussion_href, msg)

        notification_class = 'info' if msg else 'success'
        values = {
            'msg': msg if msg else no_messages,
            'notification_class': notification_class
        }
        return json.dumps(values)