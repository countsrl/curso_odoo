# -*- coding: utf-8 -*-
{
    'name': "Management Hotel",
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
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'views/hostal_menus.xml',

        'views/room_property_tags.xml',
        'data/tags_data.xml',
        'security/security.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False
}
