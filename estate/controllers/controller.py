from odoo import http
from odoo.http import request, route


class Request(http.Controller):
    @route(['/list_property'], type="http", auth="user", website=True)
    def list_property(self):
        properties = request.env['estate.property'].sudo().search([])

        values = {
            'list_properties': properties
        }

        return http.request.render('estate.request_list', values)
