from odoo import fields, models, api


class Services(models.Model):
    _name = 'service'
    _description = 'Hostel Services'

    # Constrains
    _sql_constraints = [('name_uniq', 'unique (name)', 'A property tag name  must be unique !')]
    _order = "name"

    name = fields.Char('Title', required=True)
    color = fields.Integer('Color')
