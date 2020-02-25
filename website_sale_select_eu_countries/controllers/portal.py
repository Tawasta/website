
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class Extension(CustomerPortal):

    @route()
    def account(self, redirect=None, **post):
        res = super(Extension, self).account(redirect=None, **post)
        europe = request.env.ref('base.europe').country_ids
        res.qcontext['countries'] = europe
        return res
