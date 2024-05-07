from odoo import fields, models

class ResUsers(models.Model):
    _name = 'res.users'
    _description = 'User'
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id', string='Properties')