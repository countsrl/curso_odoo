# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = _('Property Type')
    _order = 'sequence, name'
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
        
    ]

    name = fields.Char(_('Property Type'), required=True)
    sequence = fields.Integer('Sequence', default=10)
    property_ids = fields.One2many('estate.property','property_type_id', string='Properties')
