# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = _('Estate_property_offer')

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[
            ("accepted", "Accepted"), 
            ("refused", "Refused ")
            
        ],
        string = "Status",        
        copy=False,
        default= "accepted",)
      
    partner_id = fields.Many2one("res.partner",string = "Partner",required=True)  
    property_id = fields.Many2one("estate.property",string = "Property", required=True)
    
    
        
