# -*- coding: utf-8 -*-

{
    'name': "Curso Countigo",
    'version': '1.0',
    'category': 'Sales/Sales',
    'sequence': 1,
    'description': """ Modulo para el curso de Odoo Countigo SURL """,
    'summary': """ Modulo para el curso de Odoo Countigo SURL """,
    'author': "Rafael V. Barrientos Holder",
    'website': '',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'view/curso_countigo_property_views.xml',
        'view/curso_countigo_property_menus.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
