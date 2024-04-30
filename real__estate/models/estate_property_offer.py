# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from datetime import timedelta, date


_logger = logging.getLogger(__name__)


class Estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = _('Estate_property_offer')
    
        
    _sql_constraints = [('positive_price_offer', 'CHECK(price > 0)',
                         'The expected price must be strictly positive'),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[
            ("accepted", "Accepted"), 
            ("refused", "Refused ")
            
        ],
        string = "Status",        
        copy=False,
        )
      
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string= "Dead Line", compute='_compute_date_deadline' , inverse='_inverse_date_deadline', store=True)


    create_date = fields.Date(default=lambda self: fields.Date.today())     
    partner_id = fields.Many2one("res.partner",string = "Partner",required=True)  
    property_id = fields.Many2one("estate.property",string = "Property", required=True)
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date: # Verifica si create_date tiene un valor
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:  # Verifica si create_date tiene un valor
                record.validity =(record.date_deadline - record.create_date).days
    
    
    #linkeando button  “Accept” and “Refuse” to the estate.property.offer model.
        
    def action_accept(self):          
        self.write({'status': 'accepted'})
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.status = 'offer_accepted'
    
    def action_refused(self):
        self.write({'status': 'refused'})
        self.property_id.buyer_id = ''
        self.property_id.selling_price = '0.0'
        self.property_id.status = 'cancel'
        
        


    
    
    
        
