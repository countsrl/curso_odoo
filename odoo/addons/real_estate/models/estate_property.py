from odoo import models, fields
from datetime import timedelta, date

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _rec_name = 'name' 

    name = fields.Char(required=True)  # Campo obligatorio
    description = fields.Text()
    postcode = fields.Char()
    title = fields.Char(string='Title')
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=90))  # Esto establece el valor predeterminado del campo. lambda self: es una función anónima en Python. fields.Date.today() obtiene la fecha actual y timedelta(days=90) añade 90 días a esa fecha.
    expected_price = fields.Float(required=True, copy=False)  # Campo obligatorio y prevenir la copia de este campo
    selling_price = fields.Float(readonly=True)  # Campo de solo lectura
    bedrooms = fields.Integer(default=2)  # Valor predeterminado de 2
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)  # añade campo activo con valor predeterminado
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
      
    ], default='new')