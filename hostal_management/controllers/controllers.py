from odoo import http
from odoo.http import request


class Controller(http.Controller):
    @http.route('/hostal/reservation', type='http', auth='public', website=True)
    def list(self, **kw):
        reservations = request.env['hostal.reservation'].sudo().search([])

        values = {
            'reservations': reservations
        }

        return request.render('hostal_management.reservations_list', values)

        
    
   
