from odoo import fields, models, api


class PropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'

    # Constrains
    _sql_constraints = [('name_uniq', 'unique (name)', 'A property tag name  must be unique !')]
    _order = "name"

    name = fields.Char('Title', required=True)
    color = fields.Integer('Color')
