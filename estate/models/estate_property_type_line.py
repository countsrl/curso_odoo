from odoo import models, fields


class PropertyTypeLine(models.Model):
    _name = 'estate.property.type.line'
    _description = 'Estate Property Type'

    model_id = fields.Many2one("estate.property.type")
    name = fields.Char('Title')
    expected_price = fields.Float('Expected Price')
    status = fields.Selection(
        [('nuevo', 'Nuevo'), ('oferta_rec', 'Oferta Recibida'), ('oferta_acep', 'Oferta Aceptada'),
         ('vendido', 'Vendido'), ('cancelado', 'Cancelado')], 'Status', default='nuevo')
