# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from datetime import timedelta, date
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"   
   
    
    name = fields.Char(string="Title", required=True)       
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90)) 
    expected_price = fields.Float(string="Expected Prices", required=True, copy=False)
    selling_price = fields.Float(string="Selling prices", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default="2")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facade")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string='Garden Area')
    active = fields.Boolean(default=True) 
    garden_orientation = fields.Selection([('n', 'North'), ('s', 'South'), ('e', 'East'), ('w', 'West')], string="Garden Orientation", default="n" )
    total_area = fields.Integer(string='Total Area' , 
                                    compute='_compute_total_area')
    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ("offer_accepted", "Offer Accepted "),
        ("sold", "Sold"),
        ("cancel", "Cancelled"),      
    ], default='new')
      
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")   
    tag_ids = fields.Many2many("estate.property.tag", string= "Tags")
    user_id = fields.Many2one("res.users",string = "Seller", default= lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner",string = "Buyer",copy=False, readonly=True)
    offer_ids = fields.One2many("estate.property.offer","property_id", string= "Offer")
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
 
  
    
    
  # fields compute use Calcular el area total
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area    
    
    
   # onchange use al marcar garden por defecto garden_area sea 10 y orintacion norte
    @api.onchange('garden')
    def _onchange_is_garden(self):   
        if self.garden == True:
            self.garden_area = '10'
            self.garden_orientation = "n"
        else:
            self.garden_area = '0'
            self.garden_orientation = ""
            
    #use mapped function for max value for many2one list
    @api.depends('offer_ids.price')     
    def _compute_best_price(self):        
        for record in self:
            if record.offer_ids:
                record.best_price =max(record.offer_ids.mapped('price'))
            else:
                record.best_price="0.00"
    
    #linkeando button
        
    def action_sold(self):
        for record in self:
            if self.status == "cancel":
                raise ValidationError(
                _("Cancelled properties can not be sold."))
            else:
                record.status = "sold"
        return True
    
    def action_cancelled(self):
        for record in self:
            if self.status == "sold":
                raise ValidationError(
                _("Sold properties can not be cancelled."))
            else:
                record.status = "cancel"
        return True
    
    

        
        
        
    
  

    
 