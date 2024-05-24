from odoo import models, fields

class Client(models.Model):
    _name = 'hostel.client'
    _description = 'Cliente del Hostel'
    
    
    # Basic feelds 
    name = fields.Char('Nombre', required=True)
    surname = fields.Char('Apellido', required=True)
    email = fields.Char('Correo Electrónico', required=True)
    phone = fields.Char('Teléfono', required=True)
     
     # Relations
    reservation_ids = fields.One2many('hostel.reservation', 'client_id', string='Reservas')
    