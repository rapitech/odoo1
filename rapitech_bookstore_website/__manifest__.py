# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Bookstore',
    'version': '1.3',
    'category': 'Website Sale',
    'depends': ['website_sale','website','base','rapitech_bookstore_products','product'],
    'description': """
        Extension para website de librería
    """,
    'data': [
        #'security/ir.model.access.csv',
        'views/view.xml',
        'views/template.xml',
    ],
    'installable': True,
    'auto_install': False,
}