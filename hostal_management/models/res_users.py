# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Users(models.Model):
    
    _inherit = 'res.users'    
    _name = 'res.users'
    _description = 'User'
    
    hostal_ids=fields.One2many('hostal', 'user_id', string='Hostal')
    

