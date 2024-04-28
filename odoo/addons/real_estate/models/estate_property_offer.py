from odoo import models, fields,api
from datetime import timedelta, date
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Offer Price')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')  

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):  # <-- Esta es la función que calcula el 'date_deadline'
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):  # <-- Esta es la función inversa para el 'date_deadline'
        for record in self:
            if record.create_date and record.date_deadline:
                  create_date = record.create_date.date()  # Convertir a datetime.date
            record.validity = (record.date_deadline - create_date).days