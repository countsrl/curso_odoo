import datetime
from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    # Constrains
    _sql_constraints = [('check_price', 'CHECK(price > 0)',
                         'El precio de oferta de una propiedad debe ser estrictamente positivo')]
    _order = "price desc"

    price = fields.Float('Price')
    state = fields.Selection([('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], 'State', copy=False)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_date')
    create_date = fields.Date()

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for rec in self:
            rec.create_date = datetime.datetime.now().date()
            rec.date_deadline = rec.create_date + datetime.timedelta(days=rec.validity)

    def _inverse_date(self):
        for rec in self:
            rec.date_deadline = datetime.datetime.now().date() + datetime.timedelta(days=rec.validity)
            rec.create_date = datetime.datetime.now().date()

    def action_rechazar(self):
        self.state = 'rechazado'
        self.property_id.buyer = ''
        self.property_id.sale_price = ''
        self.property_id.state = 'nuevo'

    def action_aceptar(self):
        self.state = 'aceptado'
        self.property_id.buyer = self.partner_id
        self.property_id.sale_price = self.price
        self.property_id.state = 'oferta_acep'
