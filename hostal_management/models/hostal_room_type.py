# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Hostal_room_type(models.Model):
    _name = 'hostal.room.type'
    _description = 'Room Type'
    
    name = fields.Char(string="Tipo de Habitacion", required=True)
    description=fields.Text(string="Descripcion")
    room_ids=fields.One2many("hostal.room", "room_type_id", string="Hotel Room")
