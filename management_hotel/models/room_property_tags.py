from odoo import fields, models, api


class RoomPropertyTags(models.Model):
    _name = 'room.property.tags'
    _description = 'Room Property Tags'

    # Constrains
    _sql_constraints = [('name_uniq', 'unique (name)', 'The property tag name  must be unique !')]
    _order = "name"

    name = fields.Char('Title', required=True)
    color = fields.Integer('Color')
