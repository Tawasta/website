# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Jarmo Kortetjärvi
#    Copyright 2015 Oy Tawasta OS Technologies Ltd.
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Website Large Header',
    'category': 'Theme',
    'version': '8.0.0.1.0',
    'author': 'Oy Tawasta OS Technologies Ltd.',
    'license': 'AGPL-3',
    'website': 'http://www.tawasta.fi',
    'depends': [
        'website',
        'website_logo',
    ],
    'data': [
        'views/style.xml',
        'views/header.xml',
    ],
    'application': True,
}
