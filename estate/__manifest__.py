# -*- coding: utf-8 -*-
{
    'name': ' Real Estate',
    'category': 'Real Estate/ Brokerage',
    'version': '17.0.1.0',
    'description': """ Estate Description """,
    'summary': """ Estate Summary """,
    'author': '',
    'website': '',
    'category': '',
    'depends': ['base', 'web', 'website'],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_views.xml",
        "views/templates.xml",
        "views/estate_menu.xml",
        "security/ir.model.access.csv",
        "report/estate_property_templates.xml",
        "report/estate_property_report.xml",
        
    ],'assets': {
            'web.assets_backend': [
                'estate/static/src/**/*'
            ],
        },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
