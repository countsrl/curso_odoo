# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Hostal(models.Model):
    _name = 'hostal'
    _description = _('Hostal')

    name = fields.Char(string="Nombre del Hostal")
    description = fields.Text(string="Descripcion")
    adress = fields.Char(string="Direccion")
    user_id = fields.Many2one("res.users",string = "Contacto", default= lambda self: self.env.user)
    room_ids = fields.One2many("hostal.room", "hostal_id", string = "Habitacion", store=True)
    services_ids = fields.One2many("hostal.services", "hostal_service_id", string = "Servicio de Hostal", store=True)
    image_hostal = fields.Binary(string='Hostal Image')
     #servicios
    internet_serv = fields.Selection([
        ('pay', 'Si, de pago'),
        ('free', 'Si, gratis'),
        ('no', 'No'),
    ], string='Internet', placeholder="Servicio de Internet")
    
    parking_serv = fields.Selection([
        ('pay', 'Si, de pago'),
        ('free', 'Si, gratis'),
        ('no', 'No'),
    ], string='Aparcamiento', placeholder="Servicio de aparcamiento")
    
    restaurant_serv = fields.Boolean(string="Restaurante")
    bar_serv = fields.Boolean(string="Bar")
    pool_serv = fields.Boolean(string="Piscina")
    garden_serv = fields.Boolean(string="Jardin")
    smoking_area = fields.Boolean(string="Area para fumadores")

    
   
   

   
