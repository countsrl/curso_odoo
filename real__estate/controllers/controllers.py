# -*- coding: utf-8 -*-
# from odoo import http


# class RealEstate(http.Controller):
#     @http.route('/real__estate/real__estate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/real__estate/real__estate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('real__estate.listing', {
#             'root': '/real__estate/real__estate',
#             'objects': http.request.env['real__estate.real__estate'].search([]),
#         })

#     @http.route('/real__estate/real__estate/objects/<model("real__estate.real__estate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('real__estate.object', {
#             'object': obj
#         })
