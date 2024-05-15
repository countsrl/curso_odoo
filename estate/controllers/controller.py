from odoo import http
from odoo.http import request


class Controller(http.Controller):
    @http.route('/estate', type='http', auth='public', website=True)
    def list(self, **kw):
        properties = request.env['estate.property'].sudo().search([])

        values = {
            'properties': properties
        }

        return request.render('estate.property_list', values)

        
    
   
