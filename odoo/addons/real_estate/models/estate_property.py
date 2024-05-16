from odoo import models, fields, api
from datetime import timedelta, date
from datetime import datetime
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _rec_name = 'name' 
    _order = 'id desc'

    # Basic fields
    name = fields.Char(string='Name')
    title = fields.Char(string='Title')
    active = fields.Boolean(default=True)  # Campo activo con valor predeterminado a True, utilizado para filtrar propiedades activas.
    description = fields.Text() 
    
    # Price fields
    expected_price = fields.Float(required=True, copy=False)  # Campo obligatorio, no se copia
    selling_price = fields.Float(readonly=True)  # Campo de solo lectura

    # Property details
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()

    # Garden details
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])

    # Other details
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90))  # Esto establece el valor predeterminado del campo. lambda self: es una función anónima en Python. fields.Date.today() obtiene la fecha actual y timedelta(days=90) añade 90 días a esa fecha.
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('canceled', 'Canceled'),
        ('sold', 'Sold'),
      ], required=True, copy=False, default='new')
      
    # Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    # Relations
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', ondelete='cascade')  
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)  
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)  # represent vendedor
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='User') 
 
    # function
    def action_sold(self):
        pass
        _logger.debug(f"Estado de la propiedad antes de vender: {self.state}")
        #if self.state == 'offer_accepted':
            #self.state = 'sold'
        #else:
            #raise UserError("Onlyj properties with 'Offer Accepted' state can be sold.")
    #def action_sold(self):
        #for prop in self:
            #if prop.state == 'sold':
                #continue  # Evita cambiar el estado si ya está vendido
            #if prop.state != 'offer_accepted':
                #raise UserError("Only properties with 'Offer Accepted' state can be sold.")
    def action_accept_offer(self):
        self.state = 'offer_accepted'
    def action_offer_received(self):
        self.state = 'offer_received'
    def action_cancel(self):
        if self.state == 'sold':
            raise UserError("A sold property cannot be canceled.")
        self.state = 'canceled'

    # camp Compute
    @api.depends('living_area', 'garden_area')  # This decorator specifies the field dependencies for the compute method.
    def _compute_total_area(self):
        """Compute the total area based on the living area and the garden area."""
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')   # This decorator specifies the field dependencies for the compute method.
    def _compute_best_offer(self):
        """Compute the best offer based on the prices of the offers."""
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)
    @api.onchange('garden')
    def _onchange_garden(self):
        """Method that is invoked when the value of the 'garden' field changes."""
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = False
   