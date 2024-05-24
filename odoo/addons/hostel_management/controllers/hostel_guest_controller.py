from datetime import datetime
from odoo.http import Controller, route, request

class HostelGuestController(Controller):
    
    @route('/report/guests/stay_duration/<int:days>', type='http', auth='user', website=True)
    def report_guests_stay_duration(self, days):
     reservations = request.env['hostel.reservation'].sudo().search([])
     guest_ids = [guest.id for reservation in reservations for guest in reservation.guest_ids if (reservation.check_out_date - reservation.check_in_date).days == days]
     docs = request.env['hostel.guest'].sudo().search([('id', 'in', guest_ids)])
     valor = {
         'show_guest': True,
        'docs': docs
     }
     return request.render('hostel_management.website_layout_inherit', valor)

    @route('/report/guests/room_type/<string:room_type>', type='http', auth='user', website=True)
    def report_guests_room_type(self, room_type):
       reservations = request.env['hostel.reservation'].sudo().search([('room_id.room_type', '=', room_type)])
       guest_ids = [guest.id for reservation in reservations for guest in reservation.guest_ids]
       docs = request.env['hostel.guest'].sudo().search([('id', 'in', guest_ids)])
       valor = {
           'show_guest': True,
        'docs': docs
       }
       return request.render('hostel_management.website_layout_inherit', valor)
   
    @route('/report/all_guests', type='http', auth='user', website=True)
    def report_all_guests(self):
        docs = request.env['hostel.guest'].sudo().search([])
        valor = {
            'show_guest': True,
        'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)
    
    @route('/report/guest/<int:guest_id>', type='http', auth='user', website=True)
    def report_guest(self, guest_id):
        doc = request.env['hostel.guest'].sudo().browse(guest_id)
        valor = {
            'show_guest': True,
        'docs': [doc]
         }
        return request.render('hostel_management.website_layout_inherit', valor)
    @route('/report/guests_with_nationality/<string:nationality>', type='http', auth='user', website=True)
    def report_guests_with_nationality(self, nationality):
        docs = request.env['hostel.guest'].sudo().search([('nationalitys.name', '=', nationality)])
        valor = {
            'show_guest': True,
        'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)
    @route('/report/guests/page/<int:page>', type='http', auth='user', website=True)
    def report_guests_page(self, page=1, page_size=20):
        offset = (page - 1) * page_size
        docs = request.env['hostel.guest'].sudo().search([], offset=offset, limit=page_size)
        valor = {
            'show_guest': True,
        'docs': docs
        }
        return request.render('hostel_management.report_hostel_guest', valor)



    
   
    
    




