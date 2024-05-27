# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Room_amenities(models.Model):
    _name = 'room.amenities'
    _order = 'sequence, name'
    _description = _('Room amenities')
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
        
    ]

    name = fields.Char(_('Amenities'), required=True)
    sequence = fields.Integer("Sequence", default=10)
