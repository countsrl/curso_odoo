from odoo.http import Controller, route, request

class EstateController(Controller):
    
    @route('/mi_index', auth='public')
    def index(self, **kw):
        return "Welcome to my website..."

    @route('/report/properties', type='http', auth='user', website=True)
    def report_properties(self):
        docs = request.env['estate.property'].sudo().search([])
        valor = {
            'docs': docs
        }
        return request.render('real_estate.report_property_offers', valor)
    
    @route('/estate/properties', type='http', auth='user', website=True)
    def list_properties(self):
        docs = request.env['estate.property'].sudo().search([])
        valor = {
            'docs': docs,
            'show_property_offers': True,
            'show_all_properties': False,
        }
        return request.render('real_estate.website_layout_inherit', valor)
     
    @route('/estate/user_list_properties', type='http', auth='user', website=True)
    def user_list_properties(self):
        users = request.env['res.users'].sudo().search([])
        valor = {
            'docs': users,
            'show_property_offers': False,
            'show_all_properties': True,
        }
        return request.render('real_estate.website_layout_inherit', valor)

    @route('/estate/user_properties/<int:user_id>', type='http', auth='user', website=True)
    def users_properties(self, user_id):
        user = request.env['res.users'].sudo().browse(user_id)
        valor = {
            'docs':  user,
            'show_property_offers': False,
            'show_all_properties': True,
        }
        return request.render('real_estate.website_layout_inherit', valor)

           