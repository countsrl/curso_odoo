from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type' 
    _order = "sequence"
    
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    
    property_ids = fields.One2many("estate.property", "property_type_id")