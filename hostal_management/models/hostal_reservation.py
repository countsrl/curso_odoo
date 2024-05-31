# -*- coding: utf-8 -*-
import logging

import datetime

from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class HostalReservation(models.Model):
    _name = 'hostal.reservation'
    _order = "name"
    _rec_name = 'date_reservation'
    _description = _('Hostal Reservation')
    _sql_constraints = [
        ("check_number_of_guest", "CHECK(number_of_guest > 0)", "The number_of_guest must be strictly positive"),
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]


    name = fields.Char(_('Reservation No'), readonly=True,
                               default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Guest')
    number_of_guest = fields.Integer(default=1, string="Number of Guest")
    invoice_id = fields.Many2one("account.move")
    payment_status = fields.Boolean(default=False, compute='_compute_payment_status')
    total_price = fields.Integer('Total price', compute='_compute_total_price', store=True)
    room_ids = fields.Many2many('rooms', string='Room')
    # room_ids = fields.Many2many(comodel_name="rooms", rel="reservation.room.rel", 
    #                 column1="reservation_id", column2="room_id", string="Rooms") 
    date_reservation = fields.Datetime('Date Reservation', readonly=True, 
                                        default = lambda self: fields.Datetime.now())
    check_in = fields.Date('Date Check In', required=True)
                               
                               
                                
    check_out = fields.Date('Date Check Out', required=True)
                                
    
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('booked', 'Booked'),
            ('check_in', 'Check in'),
            ('check_out', 'Check out'),
            ('cancel', 'Cancel')
        ],
        string="Status",        
        default="draft",
        readonly=True,
    )

    partner_ids = fields.One2many('hostal.partner.lines', 'reservation_id', string='Guest information')


    def select_check_in(self):
        for record in self:
            if record.number_of_guest == len(self.partner_ids):
                record.state = 'check_in'
                record.room_ids.state = 'occupied'
                journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
                invoice = self.env['account.move'].create({
                'partner_id': self.partner_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                        Command.create({
                            "name": record.name,
                            "quantity": 1.0,
                            "price_unit": record.total_price,
                        }),
                        
                    ],
                })

                return {
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'account.move',
                        'type': 'ir.actions.act_window',
                        'res_id': invoice.id,
                        'target': 'current',
                    }
            else:
                raise UserError(_("Please provide all guest information"))            
            return True


    @api.onchange('check_in')
    def onchange_check_in(self):
        self._auto_assign_check_out()
        self._check_availability()

    @api.onchange('check_out')
    def onchange_check_out(self):
        self._auto_assign_check_in()
        self._check_availability()

    @api.onchange('room_ids')
    def onchange_room(self):        
        self._check_availability()

    def select_check_out(self):     

        self.state = 'check_out'
        self.room_ids.state = 'available'

    def action_cancel(self):
         self.write({'state':'cancel'})

    @api.depends('invoice_id.payment_state')
    def _compute_payment_status(self):
        for rec in self:
            if rec.invoice_id.payment_state == 'paid':
                rec.payment_status = True
            else:
                rec.payment_status = False

    @api.depends('check_in', 'check_out', 'room_ids.rent')
    def _compute_total_price(self):
        self.total_price = 0
        if self.check_out and self.check_in and self.room_ids:
            selected_room_ids = self.room_ids
            
            for rec in selected_room_ids:            
                    days = (self.check_out - self.check_in).days                
                    self.total_price += days * rec.rent 

    @api.model
    def create(self, vals):         
        
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'reservation_sequence') or _('New')

        vals['state'] = 'booked'
        
        res = super().create(vals)

        return res
        

    @api.constrains('number_of_guest','room_ids.capacity')
    def check_as_capacity(self):
        for rec in self:
            sum_value = sum(rec.room_ids.mapped("capacity"))
            if rec.number_of_guest > sum_value:
                raise ValidationError('The number of guests exceeds the capacity of the rooms.')
    
    @api.constrains('check_in','check_out')
    def check_as_reservation_today(self):
        for record in self:
            if record.check_in < datetime.date.today():
                raise ValidationError('The entry date is not correct')
            if record.check_out < datetime.date.today():
                raise ValidationError('The out date is not correct')
            

    def _auto_assign_check_in(self):
        if self.check_out:
            if not self.check_in or (self.check_in and self.check_out < self.check_in):
                self.check_in = self.check_out - datetime.timedelta(days=1)
                
    def _auto_assign_check_out(self):
        if self.check_in:
            if not self.check_out or (self.check_out and self.check_out < self.check_in):
                self.check_out = self.check_in + datetime.timedelta(days=1)
                
    def _check_availability(self):
        pass        
        selected_room_ids = self.room_ids
        for rooms in selected_room_ids:
            #value= rooms.ids
            is_reservation_exist = self.env['hostal.reservation'].search([
                ('room_ids', '=', rooms.ids),            
                ('check_in', '<=', self.check_in),
                ('check_out', '>=', self.check_in),
                ('state', 'in', ['booked', 'check_in']),
            ])
            # value = rooms.id.origin
            # is_reservation_rooms_exist = self.env['hostal.reservation'].search([                
            #     ('room_ids.rooms_id', '=', rooms.id),
                
            # ])
            if is_reservation_exist:
                raise ValidationError(_("Room %s is not available on %s") % (rooms.name, self.check_in))                        