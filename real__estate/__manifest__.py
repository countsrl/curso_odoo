# -*- coding: utf-8 -*-
{
    'name': "Real_Estate",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Descripcion del modulo
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Real Estate Property',
    'version': '16.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menu.xml",
        "views/estate_property_offer_views.xml",
        "security/ir.model.access.csv"
    ],
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    #'demo': [
     #   'demo/demo.xml',
    #],
    'license': 'LGPL-3',
}
