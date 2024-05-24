from odoo import http
from odoo.http import Controller, request, route

class HostelReservationController(Controller):
    
    
 @route('/report/all_reservations', type='http', auth='user', website=True)
 def report_all_reservations(self):
    docs = request.env['hostel.reservation'].sudo().search([])
    valor = {
        'show_all_reservations': True,
        'docs': docs
    }
    return request.render('hostel_management.website_layout_inherit', valor)

 @route('/report/reservations/page/<int:page>', type='http', auth='user', website=True)
 def report_reservations_page(self, page=1, page_size=20):
        offset = (page - 1) * page_size
        docs = request.env['hostel.reservation'].sudo().search([], offset=offset, limit=page_size)
        valor = {
            'show_all_reservations': True,
        'docs': docs
        }
        return request.render('hostel_management.report_hostel_reservation', valor)
@route('/report/reservations/draft', type='http', auth='user', website=True)
def report_reservations_draft(self):
    reservations = request.env['hostel.reservation'].sudo().search([('state', '=', 'draft')])
    valor = {
        'show_all_reservations': True,
        'reservations': reservations
    }
    return request.render('hostel_management.website_layout_inherit', valor)

@route('/report/reservations/done', type='http', auth='user', website=True)
def report_reservations_done(self):
    docs = request.env['hostel.reservation'].sudo().search([('state', '=', 'done')])
    valor = {
        'show_all_reservations': True,
        'docs': docs
    }
    return request.render('hostel_management.website_layout_inherit', valor)

@route('/report/reservations/num_persons/<int:num_persons>', type='http', auth='user', website=True)
def report_reservations_num_persons(self, num_persons):
    docs = request.env['hostel.reservation'].sudo().search([('num_persons', '=', num_persons)])
    valor = {
        'show_all_reservations': True,
        'docs': docs
    }
    return request.render('hostel_management.report_hostel_reservation', valor)
@http.route('/report/bookings/state/<string:state>', type='http', auth='user', website=True)
def report_bookings_state(self, state):
    if state not in ['draft', 'confirmed', 'done', 'cancelled']:
        return "Estado inválido"
    reservations = request.env['hostel.reservation'].sudo().search([('state', '=', state)])
    return request.render('hostel_management.website_layout_inherit', {
        'show_all_reservations': True,
        'docs': reservations
    })
@route('/report/reservations/client/<int:client_id>', type='http', auth='user', website=True)
def report_reservations_client(self, client_id):
        if client_id <= 0:
            return "ID de cliente inválido"
        docs = request.env['hostel.reservation'].sudo().search([('client_id', '=', client_id)])
        valor = {
            'show_all_reservations': True,
            'docs': docs
        }
        return request.render('hostel_management.report_all_reservations', valor)






