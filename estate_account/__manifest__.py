# -*- coding: utf-8 -*-
{
    'name': "Estate Account",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Daniela Rivera Feria",
    'website': " ",
    'application': True,
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'estate'],

    # always loaded
    'data': [
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False
}
