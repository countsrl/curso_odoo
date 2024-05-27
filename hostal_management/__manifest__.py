# -*- coding: utf-8 -*-
{
    "name": " Hostal Management",
    "category": "Hostal Management/",
    "version": "17.0.1.0",
    "description": """ Hostal Management Description """,
    "summary": """ Hostal Management Summary """,
    "author": "",
    "website": "",
    "depends": ["base","account"],
    "data": [
        'security/security_groups.xml',
        "security/ir.model.access.csv",
        "views/room_amenities_views.xml",
        "views/room_floor_views.xml",
        "views/rooms_views.xml",
        "views/res_partner_views.xml",
        "views/hostal_reservation_views.xml",
        "data/hostal_accommodation_sequence_number.xml",
        
        "views/hostal_menu.xml"
    ],
    "assets": {
        "web.assets_backend": ["hostal_management/static/src/**/*"],
    },
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}

