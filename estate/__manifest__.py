# -*- coding: utf-8 -*-
{
    'name': "Mi Real Estate",
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
    'depends': ['base', 'product', 'website'],

    # always loaded
    'data': [
        'views/estate_property_offer_view.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_view.xml',
        'views/estate_menus.xml',
        'security/security.xml',
        'reports/estate_property_templates.xml',
        'reports/estate_property_reports.xml',
        'templates/portal_web_estate.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False
}
