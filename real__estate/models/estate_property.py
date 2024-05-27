# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from datetime import timedelta, date
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare, float_is_zero


_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"   
    
    #constraint
    _sql_constraints = [('positive_price', 'CHECK(expected_price > 0)',
                         'The expected price must be strictly positive'),
                        ('positive_selling_price', 'CHECK(selling_price >= 0)',
                         'The selling price must be strictly positive'),]
   
    
    name = fields.Char(string="Title", required=True)       
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90)) 
    expected_price = fields.Float(string="Expected Prices", required=True, copy=False)
    selling_price = fields.Float(string="Selling prices",readonly=True)
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
    ], default='new', readonly=True)
      
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")   
    tag_ids = fields.Many2many("estate.property.tag", string= "Tags")
    user_id = fields.Many2one("res.users",string = "Salesman", default= lambda self: self.env.user)
   
    buyer_id = fields.Many2one("res.partner",string = "Buyer",readonly=True)
    offer_ids = fields.One2many("estate.property.offer","property_id", string= "Offer", store=True)
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
  
    
    
  
        
    # Calcular el area total   
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area  
    
    
   # onchange al marcar garden por defecto garden_area sea 10 y orintacion norte
    @api.onchange('garden')
    def _onchange_is_garden(self):   
        if self.garden == True:
            self.garden_area = '10'
            self.garden_orientation = "n"
        else:
            self.garden_area = '0'
            self.garden_orientation = ""
            
    #Calcular valor maximo de una lista one2many usando funtion mapped and function max.
    @api.depends('offer_ids.price')     
    def _compute_best_price(self):        
        for record in self:
            if record.offer_ids:
                record.best_price =max(record.offer_ids.mapped('price'))
            else:
                record.best_price="0.00"
    
    # linkeando button cancel or set a property as sold.
    # A canceled property cannot be set as sold, and a sold property cannot be canceled.
    # use the UserError function.
        
    def action_sold(self):
        for record in self:
            if self.status == "cancel":
                raise ValidationError(
                _("Cancelled properties can not be sold."))
            elif self.status == "offer_accepted":
                record.status = "sold"
            else:
                 raise ValidationError(
                _("This property has no accepted offer"))
        return True
    
    def action_cancelled(self):
        for record in self:
            if self.status == "sold":
                raise ValidationError(
                _("Sold properties can not be cancelled."))
            else:
                record.status = "cancel"
        return True
    
    #It should not be possible to delete a property which is not new or canceled.
    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancel(self):
        for record in self:
            if record.status not in ['new', 'cancel']:
                raise ValidationError(
                _("Only new and cancelled properties can be deleted."))
    
    
    
 
   # the selling price cannot be lower than 90% of the expected price.
   #@api.constrains()
   #verifico si selling_price es cero o no. Si es cero, no aplicamos la restricción ya que el producto aún no tiene un precio de venta válido.
   #comparo selling_price con el 90% del expected_price. Si es menor que el 90%, se lanza una excepción de validación         
   
    @api.constrains('selling_price', 'expected_price')
    def check_price(self):
        for record in self:
           if not float_is_zero(record.selling_price, precision_digits=2) and\
            float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")
            
 
  
    

    
                
  

            
        
    
 