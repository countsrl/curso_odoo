# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request





class RoomController(http.Controller):

    @http.route('/rooms', type='http', auth='public', website=True)
    def list_rooms(self, **kwargs):
        rooms = request.env['hostal.room'].sudo().search([])
        valor ={
            'rooms':rooms
        } 
        return http.request.render('hostal_management.room_list_template', valor)
    
class WebsiteReservation(http.Controller):

    @http.route('/reservation', type='http', auth="public", website=True)
    def reservation_form(self, **kwargs):
        return http.request.render("hostal_management.reservation_form_template", {})

    @http.route('/reservation/submit', type='http', auth="public", website=True, methods=['POST'])
    def submit_reservation(self, **kwargs):
        name = kwargs.get('customer_id')
        email = kwargs.get('customer_email')
        country = kwargs.get('customer_country')
        mobile = kwargs.get('customer_mobile')
        passport = kwargs.get('customer_passport')
        room_id = kwargs.get('room_id')
        start_date = kwargs.get('check_in_date')
        end_date = kwargs.get('check_out_date')

        customer = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'country':country,
            'mobile':mobile,
            'passport':passport,
        })

        reservation = request.env['room.reservation'].sudo().create({
            'customer_id': customer.id,
            'room_id': room_id,
            'check_in_date': start_date,
            'check_out_date': end_date,
        })

        return http.request.render("hostal_management.reservation_success_template", {'reservation': reservation})

# class HostalManagement(http.Controller):
#     @http.route('/hostal_management/hostal_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hostal_management/hostal_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hostal_management.listing', {
#             'root': '/hostal_management/hostal_management',
#             'objects': http.request.env['hostal_management.hostal_management'].search([]),
#         })

#     @http.route('/hostal_management/hostal_management/objects/<model("hostal_management.hostal_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hostal_management.object', {
#             'object': obj
#         })
