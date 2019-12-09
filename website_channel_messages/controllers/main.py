##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http
from odoo.http import request

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in


class WebsiteChannelMessagesController(http.Controller):

    @http.route(
        ['/website_channel', '/website_channel/page/<int:page>'],
        type='http',
        auth='user',
        website=True,
    )
    def website_channels(self, search='', page=1, **post):
        """
        Route to show list of all channels.

        :param search: Search query
        :param page: pager current page
        :param post: kwargs
        :return: rendered object
        """
        partner_id = request.env.user.partner_id.id
        channel_model = request.env['mail.channel']

        if not partner_id:
            return request.render('website.404')

        domain = [
            ('channel_type', '=', 'channel'),
            ('public', '=', 'private'),
            ('channel_last_seen_partner_ids.partner_id', '=', partner_id),
            '|',
            ('name', 'ilike', search),
            ('channel_last_seen_partner_ids.partner_id', 'ilike', search),
        ]
        channel_count = channel_model.search_count(domain)
        url = request.httprequest.path.split("/page")[0]
        total_count = channel_count
        pager_limit = 50
        pager = request.website.pager(
            url=url,
            total=total_count,
            page=page,
            step=pager_limit,
            scope=7,
            url_args=post
        )
        channels = channel_model.sudo().search(
            domain,
            order="id DESC",
            limit=pager_limit,
            offset=pager['offset']
        )
        search_url = request.httprequest.path + ("?%s" % search)
        message_start = abs(50 - page * pager_limit) + 1
        message_end = total_count if total_count < page * pager_limit else page * pager_limit
        visible = "{} - {} / {}".format(message_start, message_end, total_count)

        values = {
            'channels': channels,
            'pager': pager,
            'visible_channels': visible,
            'search_url': search_url,
            'current_search': search,
        }
        return request.render(
            'website_channel_messages.my_channels',
            values
        )

    @http.route(
        ['/website_channel/<int:channel_id>'],
        type='http',
        auth='user',
        website=True,
    )
    def channel_messages(self, channel_id=None, **post):
        """
        Route to show list of all channels.

        :param channel_id: Related channel ID
        :param post: kwargs
        :return: rendered object
        """
        partner_id = request.env.user.partner_id.id
        channel = request.env['mail.channel'].sudo().search([
            ('id', '=', channel_id),
            ('channel_type', '=', 'channel'),
            ('public', '=', 'private'),
            ('channel_last_seen_partner_ids.partner_id', '=', partner_id),
        ])

        if not channel:
            return request.render('website.404')

        values = {
            'channel': channel,
        }
        return request.render(
            'website_channel_messages.channel',
            values
        )

    @http.route(
        ['/website_channel/<int:channel_id>/message'],
        type='http',
        auth="user",
        website=True,
        methods=['POST']
    )
    def channel_send_message(self, channel_id=None, **post):
        """
        Message submission handler for channel

        :param channel_id: related channel ID
        :param post: submitted form payload
        """
        user = request.env.user
        channel = request.env['mail.channel'].sudo().search([
            ('id', '=', channel_id),
            ('channel_last_seen_partner_ids.partner_id', '=', user.partner_id.id),
        ])

        if not channel:
            return request.render('website.404')

        redirect_url = post.get('redirect_url')
        channel.sudo(user).message_post(
            body=post.get('comment'),
            message_type='comment',
            subtype='mail.mt_comment',
        )
        return request.redirect(redirect_url)
