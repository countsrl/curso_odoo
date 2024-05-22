# -*- coding: utf-8 -*-
{
    'name': "Hostel Managament",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'account', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/reservation_sequence_data.xml',
        # 'data/room_sequence_data.xml',
        # 'views/room_characteristics.xml',
        # 'views/room.xml',
        'views/reservations.xml',
        'views/hostel_services.xml',
        'views/hostel_menu.xml',

    ]
}
