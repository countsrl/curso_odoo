from odoo import models, fields, api
from datetime import timedelta, date
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _rec_name = 'name' 

    # Basic fields
    name = fields.Char(required=True)
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
        ('sold', 'Sold'),
        ('off_market', 'Off Market'),
    ], default='new')
   
    # Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    # Relations
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')  
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)  
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)  
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    @api.depends('living_area', 'garden_area') #se utiliza para especificar los campos de los que depende un campo calculado
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)