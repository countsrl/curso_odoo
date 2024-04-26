from odoo import fields, models, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    # Constrains
    _sql_constraints = [('name_uniq', 'unique (name)', 'A property type name  must be unique !')]
    _order = "name"

    name = fields.Char('Title', required=True)
    property_ids = fields.One2many("estate.property.type.line", 'model_id')
    sequence = fields.Integer('Sequence',  default=1)
