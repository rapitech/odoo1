# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Products Bookstore',
    'version': '1.2',
    'category': 'Sales/Sales',
    'depends': ['product','stock','purchase','sale'],
    'description': """
Extension para productos de librería
=====================================
Añade varios campos necesarios para la gestión de una librería.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'wizards/wizard.xml'
    ],
    'installable': True,
    'auto_install': False,
}