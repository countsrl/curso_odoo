# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Room_reservation_wizard(models.Model):
    _name = 'room.reservation.wizard'
    _description = "Wizard para la reservacion de habitaciones"

    check_in_date = fields.Date('Fecha de Check-In', required=True)
    check_out_date = fields.Date('Fecha de Check-Out', required=True)
    num_adult = fields.Integer('Número de Adultos', default=1)
    num_children = fields.Integer('Número de Niños', default=0)
    
    


    
    
    def find_rooms(self):
        self.ensure_one()
        Reservation = self.env['room.reservation']
        Room = self.env['hostal.room']

        # Encuentra todas las habitaciones
        all_rooms = Room.search([])

        # Filtra habitaciones que están ocupadas durante el período especificado
        occupied_rooms = Reservation.search([
            ('check_in_date', '<=', self.check_out_date),
            ('check_out_date', '>=', self.check_in_date)
        ]).mapped('room_id')

        # Filtra habitaciones disponibles
        available_rooms = all_rooms - occupied_rooms

        # Filtra por capacidad
        available_rooms = available_rooms.filtered(lambda r: r.max_adult >= self.num_adult and r.max_child >= self.num_children)

        # Crear acción para mostrar las habitaciones disponibles
        action = self.env.ref('hostal_management.action_available_rooms').read()[0]
        action['domain'] = [('id', 'in', available_rooms.ids)]
        action['context'] = {
            'default_check_in_date': self.check_in_date,
            'default_check_out_date': self.check_out_date,
        }
        return action
    
   
    
