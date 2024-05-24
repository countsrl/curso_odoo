
# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)



class Hostal_room_service_line(models.Model):
    _name = 'hostal.room.service.line'
    _description = 'Hostal Room Service Line'

    room_id = fields.Many2one('hostal.room', string='Room', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Service Product', domain=[('type', '=', 'service')], required=True)
    quantity = fields.Float(string='Quantity', default=1.0)