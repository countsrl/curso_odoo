# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Hostal_room(models.Model):
    _name = 'hostal.room'
    _description = 'Hostal Room'

    name = fields.Char(string="Numero de Habitacion", required=True)
    description=fields.Text(string="Descripcion")
    hostal_id = fields.Many2one("hostal", string= "Hostal", required=True) 
    services_ids = fields.One2many("hostal.services", "room_service_id", string = "Servicio de Habitacion", store=True)
    room_type_id = fields.Many2one("hostal.room.type", "Categoria de Habitacion", required=True, ondelete="restrict")
    max_adult = fields.Integer(string="Maximo Adulto", required=True)
    max_child = fields.Integer(string="Maximo Niño", required=True)
    price = fields.Float(string='Price per Night', required=True)
    reservation_ids = fields.One2many("room.reservation","room_id", string="Reservation", store=True )
   
    image_room = fields.Binary(string='Room Image')
    check_in_date = fields.Date('Fecha de Check-In')
    check_out_date = fields.Date('Fecha de Check-Out')
  
    #room_services_ids = fields.Many2many(
     #   "hotel.room.services", string="Room Services", help="List of room services.")
    status = fields.Selection(
        [("available", "Available"), ("occupied", "Occupied")],
        "Status",
        default="available",
    )
    capacity = fields.Integer("Capacidad", compute='_compute_total_capacity')
    
    #services
    service_line_ids = fields.One2many('hostal.room.service.line', 'room_id', string='Service Lines')


    
    @api.depends('max_adult', 'max_child')
    def _compute_total_capacity(self):
        for record in self:
            record.capacity = record.max_adult + record.max_child
    # Mostrar por defecto la habitacion, y las fechas cuando se reserve desde e resultado
    # de disponibilidad de habitacion tras realizar una busqueda por el wizard
    def reserve_room(self):
        return {
            'name': 'Reservar Habitación',
            'type': 'ir.actions.act_window',
            'res_model': 'room.reservation',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_room_id': self.id,
                'default_check_in_date': self.env.context.get('default_check_in_date'),
                'default_check_out_date': self.env.context.get('default_check_out_date'),
                
                
            }
        }
        
        
    
    
    





    

    
 
 


    
    
   

    

    

