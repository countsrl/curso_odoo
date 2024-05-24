from odoo.http import Controller, route, request

class HostelClientController(Controller):
    
    @route('/hostel.com', auth='public')
    def index(self, **kw):
        return "Welcome to my Hostel Management..."
 
    @route('/report/all_clients', type='http', auth='user', website=True)
    def report_clients(self):
        docs = request.env['hostel.client'].sudo().search([])
        valor = {
            'show_all_clients': True,
            'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)
    @route('/report/client', type='http', auth='user', website=True)
    def report_client(self):
         docs = request.env['hostel.client'].sudo().search([])
         valor = {
             'show_guest': True,
             
        'docs': docs
         }
         return request.render('hostel_management.website_layout_inherit', valor)
    @route('/report/client/<int:client_id>', type='http', auth='user', website=True)
    def report_client(self, client_id):
         doc = request.env['hostel.client'].sudo().browse(client_id)
         valor = {
             'show_guest': True,
        'docs': doc
         }
         return request.render('hostel_management.report_hostel_client', valor)
    @route('/report/clients_with_email/<string:email>', type='http', auth='user', website=True)
    def report_clients_with_email(self, email):
         docs = request.env['hostel.client'].sudo().search([('email', '=', email)])
         valor = {
             'show_guest': True,
        'docs': docs
         }
         return request.render('hostel_management.report_hostel_client', valor)
    @route('/report/clients/page/<int:page>', type='http', auth='user', website=True)
    def report_clients_page(self, page=1, page_size=20):
        offset = (page - 1) * page_size
        docs = request.env['hostel.client'].sudo().search([], offset=offset, limit=page_size)
        valor = {
            'show_all_clients': True,
        'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)
    @route('/report/clients/search/<string:query>', type='http', auth='user', website=True)
    def report_clients_search(self, query):
        docs = request.env['hostel.client'].sudo().search([('name', 'ilike', query)])
        valor = {
            'show_all_clients': True,
        'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)
    @route('/report/clients/sort/<string:field>', type='http', auth='user', website=True)
    def report_clients_sort(self, field):
        docs = request.env['hostel.client'].sudo().search([], order=field)
        valor = {
            'show_all_clients': True,
        'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)





