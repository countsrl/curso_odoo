import base64
import io
import json
import xlsxwriter

from datetime import datetime
from odoo import http, _, fields
from odoo.http import request


class Request(http.Controller):
    @http.route(['/list/availability'], type="http", auth="user", website=True)
    def list_availability(self):
        free_rooms = request.env['room'].search([('states', '=', 'disponible')])

