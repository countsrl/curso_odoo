# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Hostal_services(models.Model):
    _name = 'hostal.services'
    _description = 'Servicios'

    name = fields.Char(string="Nombre del servicio")
    description = fields.Text(string="descripcion del servicio")
    hostal_service_id = fields.Many2one("hostal", string= "Hostal") 
    room_service_id = fields.Many2one("hostal.room", string= "Room") 
    type_services = fields.Selection([('hostal', 'Hostal'), ('room', 'Habitacion')],string="Tipo de servicio", default="hostal")
   
   
