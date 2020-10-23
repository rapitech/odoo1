# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Rapitech Website Dynamic Snippet',
    'version': '1.2',
    'category': 'Website Sale',
    'depends': ['website_sale','website'],
    'description': """
        Extension para filtrar elementos en dynamic snippet
    """,
    'data': [
        #'security/ir.model.access.csv',
        'views/view.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False,
}