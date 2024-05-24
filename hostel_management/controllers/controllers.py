from odoo import http, _
from odoo.http import request


class Request(http.Controller):
    @http.route(['/list/availability'], type="http", auth="user", website=True)
    def list_availability(self):
        available_rooms = request.env['room'].search([('states', '=', 'disponible')])

        values = {
            'list_rooms': available_rooms,
        }

        return http.request.render('hostel_management.request_list', values)

    @http.route(['/list/reservations'], type="http", auth="user", website=True)
    def list_reservations(self):
        user = request.env.user.partner_id.id
        reservations = request.env['reservation'].search([('client_id', '=', user)])

        values = {
            'list_reservations': reservations,
        }

        return http.request.render('hostel_management.request_list_reservation', values)
