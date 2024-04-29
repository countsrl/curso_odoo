from odoo import models, fields

class EstateAccount(models.Model):
    _name = 'estate.account.account'
    _description = 'Property Accounts'

    name = fields.Char(string='Account Name')
    #property_id = fields.Many2one('real_estate.property', string='Related Property')