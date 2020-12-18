import base64
import logging
import werkzeug

from odoo import http, _
from odoo.exceptions import AccessError, UserError
from odoo.http import request
from odoo.addons.website_slides.controllers.main import WebsiteSlides


def slide_filter(response, filter_tags):
    # Remove any slides without any given tags
    def tag_filter(slide):
        print("-------------------KÄYKÖ TÄÄÄLLÄ----------")
        print(slide)
        print(slide.tag_ids)
        slides_tags = slide.tag_ids.mapped("name")
        print(slides_tags)
        return all(tag in slides_tags for tag in filter_tags)

    response.qcontext['slides'] = list(filter(
        tag_filter,
        list(response.qcontext['slides'])
    ))

    return response


class SlidesSearchExtended(WebsiteSlides):
    # @http.route()
    # def channel(self, *args, **kw):
    #     print("-------------------KÄYKÖ TÄÄÄLLÄ 2----------")

    #     response = super(SlidesSearchExtended, self).channel(*args, **kw)

    #     search_tags = kw.get('tags_search')
    #     if search_tags:
    #         li = search_tags.strip("[]").replace('"', "").replace(" ", "").split(",")
    #         tags = request.env["slide.tag"].sudo().search([
    #             ('id', 'in', li)
    #         ])
    #         print(tags)
    #         response.qcontext['last_chosen_tags'] = tags
    #         response = slide_filter(response, tags)

    #     # search_tags = kw.get('tags_search')
    #     # print("----------SEARCH TAGS-------")
    #     # print(search_tags)
    #     # print("----------SEARCH TAGS-------")
    #     # if search_tags:
    #     #     print("--------------------YOLOOOO-------")
    #     #     print(search_tags)
    #     #     print(int(search_tags))
    #     #     tags = request.env["slide.tag"].sudo().search([
    #     #         ('id', 'in', search_tags)
    #     #     ])
    #     #     slides = request.env["slide.slide"].sudo().search([
    #     #         ('tag_ids', 'in', tags)
    #     #     ])
    #     #     print(slides)
    #     # search = kw.get('search')
    #     # if not search:
    #     #     search_tags = None

    #     # if search_tags:
    #     #     print("---------------------IF SEARCH TAGS---------------")
    #     #     print(search_tags)
    #     #     response.qcontext['last_chosen_tags'] = search_tags
    #     #     # response = slide_filter(response, search_tags.split(","))

    #     return response

    @http.route([
        '''/slides/<model("slide.channel"):channel>''',
        '''/slides/<model("slide.channel"):channel>/page/<int:page>''',

        '''/slides/<model("slide.channel"):channel>/<string:slide_type>''',
        '''/slides/<model("slide.channel"):channel>/<string:slide_type>/page/<int:page>''',

        '''/slides/<model("slide.channel"):channel>/tag/<model("slide.tag"):tag>''',
        '''/slides/<model("slide.channel"):channel>/tag/<model("slide.tag"):tag>/page/<int:page>''',

        '''/slides/<model("slide.channel"):channel>/category/<model("slide.category"):category>''',
        '''/slides/<model("slide.channel"):channel>/category/<model("slide.category"):category>/page/<int:page>''',

        '''/slides/<model("slide.channel"):channel>/category/<model("slide.category"):category>/<string:slide_type>''',
        '''/slides/<model("slide.channel"):channel>/category/<model("slide.category"):category>/<string:slide_type>/page/<int:page>'''],
        type='http', auth="public", website=True)
    def channel(self, channel, category=None, tag=None, page=1, slide_type=None, sorting='creation', search=None, **kw):
        if not channel.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        user = request.env.user
        Slide = request.env['slide.slide']
        domain = [('channel_id', '=', channel.id)]
        pager_url = "/slides/%s" % (channel.id)
        pager_args = {}

        if search:
            domain += [
                '|', '|',
                ('name', 'ilike', search),
                ('description', 'ilike', search),
                ('index_content', 'ilike', search)]
            pager_args['search'] = search
        else:
            search_tags = kw.get('tags_search')
            if search_tags:
                li = search_tags.strip("[]").replace('"', "").replace(" ", "").split(",")
                tags = request.env["slide.tag"].sudo().search([
                    ('id', 'in', li)
                ])
                domain += [('tag_ids.id', '=', tags.ids)]
                pager_url += "/tag/%s" % tags.ids
            if category:
                domain += [('category_id', '=', category.id)]
                pager_url += "/category/%s" % category.id
            elif tag:
                domain += [('tag_ids.id', '=', tag.id)]
                pager_url += "/tag/%s" % tag.id
            if slide_type:
                domain += [('slide_type', '=', slide_type)]
                pager_url += "/%s" % slide_type

        if not sorting or sorting not in self._order_by_criterion:
            sorting = 'date'
        order = self._order_by_criterion[sorting]
        pager_args['sorting'] = sorting

        pager_count = Slide.search_count(domain)
        pager = request.website.pager(url=pager_url, total=pager_count, page=page,
                                      step=self._slides_per_page, scope=self._slides_per_page,
                                      url_args=pager_args)

        slides = Slide.search(domain, limit=self._slides_per_page, offset=pager['offset'], order=order)
        values = {
            'channel': channel,
            'category': category,
            'slides': slides,
            'tag': tag,
            'slide_type': slide_type,
            'sorting': sorting,
            'user': user,
            'pager': pager,
            'is_public_user': user == request.website.user_id,
            'display_channel_settings': not request.httprequest.cookies.get('slides_channel_%s' % (channel.id), False) and channel.can_see_full,
        }
        if search:
            values['search'] = search
            return request.render('website_slides.slides_search', values)

        # Display uncategorized slides
        if not slide_type and not category:
            category_datas = []
            for category in Slide.read_group(domain, ['category_id'], ['category_id']):
                category_id, name = category.get('category_id') or (False, _('Uncategorized'))
                category_datas.append({
                    'id': category_id,
                    'name': name,
                    'total': category['category_id_count'],
                    'slides': Slide.search(category['__domain'], limit=4, offset=0, order=order)
                })
            values.update({
                'category_datas': category_datas,
            })
        return request.render('website_slides.home', values)