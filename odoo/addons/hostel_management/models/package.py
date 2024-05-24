from odoo import api, models, fields

class Package(models.Model):
    _name = 'hostel.package'
    _description = 'Paquete del Hostal'
    _rec_name = 'name'

    # Basic fields
    name = fields.Char('Nombre del Paquete', required=True)
    price = fields.Float('Precio Total', compute='_compute_total_price', store=True)
    
    # Relations
    service_ids = fields.Many2many('hostel.service', string='Servicios Incluidos')

    @api.depends('service_ids.price')
    def _compute_total_price(self):
        for package in self:
            package.price = sum(service.price for service in package.service_ids) if package.service_ids else 0