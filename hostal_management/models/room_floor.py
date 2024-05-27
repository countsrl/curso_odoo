# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class RoomFloor(models.Model):
    _name = 'room.floor'
    _order = "name"
    _description = _('Room floor')
    _sql_constraints = [
       ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(_('Floor'), required=True)
