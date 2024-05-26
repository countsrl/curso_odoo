# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
##############################################################################

{
    'name': 'Hostal Management',
    'version': '16.0.1.0.0',
    'author': 'Roxana Lopez Velázques',
    'maintainer': 'Roxana Lopez Velázques',
    'website': '',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'summary': 'Short summary.',
    'depends': ['base','product', 'calendar','account','web','website'],
    "data": [
        "views/hostal_views.xml",
        "security/ir.model.access.csv",
        "views/hostal_room_views.xml",
        "views/room_reservation_views.xml",
        "views/hostal_menu.xml",
        "views/hostal_room_type_views.xml",
        "views/room_reservation_wizard_views.xml",
        "views/hostal_services_views.xml",
        "data/hotel_sequence.xml",
        "data/data.xml",
        "views/room_list_template.xml",
        "views/reservation_form_template.xml",
        "views/reservation_success_template.xml",
        "report/booked_report.xml",
        "report/booked_template.xml"
     
    ],
    'images': [ ],
    'installable': True,
    'application': True,
}
