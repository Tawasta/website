##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
from odoo import api, models

# 4. Imports from Odoo modules:
from odoo.tools.mail import html2plaintext

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Slide(models.Model):

    # 1. Private attributes
    _inherit = "slide.slide"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.multi
    def write(self, vals):
        """
        Copy content from website_description to index_content
        so that the content can be used for searching.

        :param vals: dict, changed values
        :return: super
        """
        if vals.get("website_description"):
            vals["index_content"] = html2plaintext(vals.get("website_description"))
        return super(Slide, self).write(vals)

    # 7. Action methods

    # 8. Business methods
