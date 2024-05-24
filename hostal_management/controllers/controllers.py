# -*- coding: utf-8 -*-
# from odoo import http


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
