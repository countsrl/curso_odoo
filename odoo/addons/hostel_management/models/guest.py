from odoo import models, fields

class Guest(models.Model):
    _name = 'hostel.guest'
    _description = 'Huésped del Hostel'
    
    #Basic Fields
    name = fields.Char('Nombre', required=True)
    nationalitys = fields.Many2one('res.country', 'Nacionalidad', required=True)
    identity_document = fields.Char('Documento de Identidad', required=True)
    sequence = fields.Integer(default=10) 
    
    #Relations 
    reservation_id = fields.Many2one('hostel.reservation', 'Reservación')
