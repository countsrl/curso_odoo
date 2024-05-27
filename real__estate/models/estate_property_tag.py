# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = _('Estate_property_tag')
    
    #constraint    
    _sql_constraints = [('unique_name', 'unique (name)', 'A property tag name  must be unique !')]
 

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color')
  