from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    # Fields
    price = fields.Float('Price')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    status = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('sold', 'Sold'),
    ], 'Status', copy=False)
    
    # Relations
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True, ondelete='cascade')
    
    # Compute and inverse methods
    @api.depends('create_date', 'validity')  # This decorator specifies the field dependencies for the compute method.
    def _compute_date_deadline(self):
        """Compute the deadline date based on the creation date and the validity period."""
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Compute the validity period based on the creation date and the deadline date."""
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = record.create_date.date()  # Converter  datetime.date
                record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
     self.status = 'accepted'
     self.property_id.state = 'sold'
     self.property_id.buyer_id = self.partner_id
     self.property_id.selling_price = self.price

    def action_refuse(self):
     self.status = 'refused'