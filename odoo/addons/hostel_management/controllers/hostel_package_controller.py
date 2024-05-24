from urllib import request
from odoo import http

class HostelPackagesController(http.Controller):

    @http.route('/report/all_packages', type='http', auth='user', website=True)
    def report_packages(self):
        packages = http.request.env['hostel.package'].sudo().search([])
        valor = {
            'show_all_packages': True,
            'packages': packages
        }
        return http.request.render('hostel_management.website_layout_inherit', valor)

    @http.route('/report/package/<int:package_id>', type='http', auth='user', website=True)
    def report_package(self, package_id):
        package = http.request.env['hostel.package'].sudo().browse(package_id)
        valor = {
            'show_all_packages': True,
            'package': package
        }
        return http.request.render('hostel_management.website_layout_inherit', valor)
@http.route('/report/packages/price_range/<int:min_price>/<int:max_price>', type='http', auth='user', website=True)
def report_packages_by_price_range(self, min_price, max_price):
    packages = http.request.env['hostel.package'].sudo().search([('price', '>=', min_price), ('price', '<=', max_price)])
    valor = {
        'show_all_packages': True,
        'packages': packages
    }
    return http.request.render('hostel_management.website_layout_inherit', valor)
@http.route('/report/package/<string:package_name>', type='http', auth='user', website=True)
def report_package_by_name(self, package_name):
    package = http.request.env['hostel.package'].sudo().search([('name', '=', package_name)], limit=1)
    valor = {
          'show_all_packages': True,
        'package': package
    }
    return http.request.render('hostel_management.website_layout_inherit', valor)
@http.route('/report/package/page/<int:page>', type='http', auth='user', website=True)
def report_package_page(self, page=1, page_size=20):
        offset = (page - 1) * page_size
        docs = request.env['hostel.package'].sudo().search([], offset=offset, limit=page_size)
        valor = {
            'show_all_packages': True,
        'docs': docs
        }
        return request.render('hostel_management.website_layout_inherit', valor)


