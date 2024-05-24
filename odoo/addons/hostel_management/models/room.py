from datetime import date
from odoo import models, fields, api

class Room(models.Model):
    _name = 'hostel.room'
    _description = 'Habitación del Hostal'
    _rec_name = 'number'

    #Basic fields 
    number = fields.Char('Número', required=True)
    sequence = fields.Integer(default=10)
    room_type = fields.Selection([
        ('single', 'Sencilla'),
        ('double', 'Doble'),
        ('suite', 'Suite')
    ], 'Tipo', required=True)
    capacity = fields.Integer('Capacidad')
    num_beds = fields.Integer('Número de Camas') 
    has_ac = fields.Boolean('Aire Acondicionado')  
    has_terrace = fields.Boolean('Terraza')  
    num_bathrooms = fields.Integer('Número de Baños') 
    price = fields.Float('Precio')
    availability = fields.Boolean('Disponibilidad')
    
    #Relations
    reservation_ids = fields.One2many('hostel.reservation', 'room_id', string='Reservas')
   
    #Camp Compute
    is_available = fields.Boolean(compute='_compute_is_available', default=True, store=True) # almacenar en la BD

    @api.depends('reservation_ids.state', 'reservation_ids.check_in_date', 'reservation_ids.check_out_date')
    def _compute_is_available(self):
        for room in self:
            room.is_available = not any(
                reservation.state == 'confirmed' and
                reservation.check_in_date <= date.today() <= reservation.check_out_date
                for reservation in room.reservation_ids
            )
