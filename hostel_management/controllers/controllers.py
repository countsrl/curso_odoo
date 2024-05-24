from odoo import http, _
from odoo.http import request


class Request(http.Controller):
    @http.route(['/list/availability'], type="http", auth="user", website=True)
    def list_availability(self):
        available_rooms = request.env['room'].search([('states', '=', 'disponible')])
        list_states = [('new', 'New'), ('confirm', 'Confirm'), ('invoice', 'Invoice'), ('invoiced', 'Invoiced'),
                       ('finished', 'Finished'), ('canceled', 'Canceled')]

        values = {
            'list_rooms': available_rooms,
            'list_states': list_states
        }

        return http.request.render('hostel_management.request_list', values)
