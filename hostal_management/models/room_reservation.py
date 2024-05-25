# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, date
from odoo.fields import Command

_logger = logging.getLogger(__name__)


class Room_reservation(models.Model):
    
    _name = 'room.reservation'
    _description = 'Reservation'

    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    room_id = fields.Many2one('hostal.room', string='Room', required=True)
    check_in_date = fields.Date(string='Check-In Date', required=True)
    check_out_date = fields.Date(string='Check-Out Date', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    customer_email = fields.Char(related='customer_id.email', string='Email', readonly=True)
    customer_country = fields.Many2one(related='customer_id.country_id', string='Pais', readonly=True)
    customer_mobile = fields.Char(related='customer_id.mobile', string='Telefono', readonly=True)
    customer_passport = fields.Char(related='customer_id.vat', string='Pasaporte', readonly=True)
    

    days_reserved = fields.Integer(string='Days Reserved', compute='_compute_days_reserved', store=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    
    
    
    state = fields.Selection([    
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('paid', 'Pagada'),
    ], string='Status', readonly=True)
   
   
    payment_status = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid')
    ], string='Payment Status', default='not_paid')
   
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('room.reservation') or 'New'
        return super(Room_reservation, self).create(vals)
    
    
    
    def action_confirm(self):
        for record in self:
            if self.state == "cancelled":
                    raise ValidationError(
                    _("Reservas canceladas no pueden confirmarse"))
            else:
                record.state = "confirmed"
        return True
                    
        

    def action_cancel(self):
        for record in self:
            if self.state == "paid":
                raise ValidationError(
                _("Reservas vendidas no pueden ser pagadas"))
            else:
                record.state = "cancelled"
        return True
    
    def action_pay(self):
        self.env['account.move'].create({
            'partner_id': self.customer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'partner_id': self.customer_id.id,
                    'price_unit': self.total_price
                }),
            ],
        })
        return super().action_pay()  
    
    
      
        
    # En el método _check_room_availability, usamos una búsqueda (search) para encontrar reservas que se solapan con la nueva reserva. La lógica incluye:
    #Comprobar que la fecha de check_in es anterior a la fecha de check_out.
    #Buscar reservas que:
    #Tengan el mismo room_id.
    #No estén canceladas.
    #No sean la misma reserva (esto es relevante en caso de ediciones).
    #Se solapen en cualquier punto con la nueva reserva. Esto se hace usando condiciones OR (|) y AND (&).
    
    @api.constrains('room_id', 'check_in_date', 'check_out_date')
    def _check_room_availability(self):
        for reservation in self:
            if reservation.check_in_date >= reservation.check_out_date:
                raise ValidationError("Check-out date must be after check-in date.")

            is_booked = self.env['room.reservation'].search([
                ('room_id', '=', reservation.room_id.id),
                ('state', '!=', 'cancelled'),
                ('id', '!=', reservation.id),
                '|', '|',
                '&', ('check_in_date', '<=', reservation.check_in_date), ('check_out_date', '>=', reservation.check_in_date),
                '&', ('check_in_date', '<=', reservation.check_out_date), ('check_out_date', '>=', reservation.check_out_date),
                '&', ('check_in_date', '>=', reservation.check_in_date), ('check_out_date', '<=', reservation.check_out_date),
            ])

            if is_booked:
                raise ValidationError("La habitacion ya esta reservada para la fecha seleccionada. Intente elegir otra fecha")
   
   
    
    @api.depends('check_in_date', 'check_out_date')
    def _compute_days_reserved(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                delta = fields.Datetime.from_string(record.check_out_date) - fields.Datetime.from_string(record.check_in_date)
                record.days_reserved = delta.days + 1

    @api.depends('days_reserved', 'room_id')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.days_reserved * record.room_id.price

    

    
   




