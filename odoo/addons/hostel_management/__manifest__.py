{
    'name': 'Hostel Management',
    'version': '1.0',
    'summary': 'Manage hostel operations',
    'license': 'LGPL-3',
    'description': """
        This module allows you to manage hostel operations, including:
        - Room management
        - Reservation management
        - Guest management
        - Invoicing
    """,
    'author': 'jasnaykel',
    'website': 'https://hostel.com',
    'category': 'Hospitality',
    'depends': ['base'],
    'data': [
        #'security/res_groups.xml',
        'security/ir.model.access.csv',
                       
        'views/client_views.xml',
        'views/hostel_room_views.xml',
        'views/hostel_reservation_views.xml',
        'views/hostel_guest_views.xml',
        'views/hostel_service_views.xml',
        'views/hostel_package_views.xml',
        'report/hostel_templates.xml',
        'report/hostel_reports.xml',
       
        'views/hostel_menu.xml',
        'views/website_layout_inherit.xml',
        
        'data/hostel_data.xml',
    ],
    'demo': [
        'demo/hostel_demo.xml',
    ],
    'installable': True,
    'application': True,
}
