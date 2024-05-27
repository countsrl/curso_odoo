# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class Estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = _('property_type')
    
    #constraint
    _sql_constraints = [('unique_name', 'unique (name)', 'A property type name  must be unique!')]
 

    name = fields.Char(_('Name', required=True))
    property_ids = fields.One2many("estate.property","property_type_id", string= "Tipo", store=True)
   
