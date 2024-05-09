# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _name = 'res.users'
    _description = _('ResUsers')
    _inherit = "res.users"


    property_ids = fields.One2many("estate.property","user_id",String = "Properties", 
                                   domain=[("state", "in", ["new", "offer_received"])])
