# -*- coding: utf-8 -*-
import logging

from datetime import timedelta

from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class HostalReservation(models.Model):
    _name = 'hostal.reservation'
    _order = "name"
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
    room_id = fields.Many2one('rooms', string='Room',domain="[('state', '!=', 'occupied')]")
    date_reservation = fields.Datetime('Date Reservation', readonly=True, 
                                        default = lambda self: fields.Datetime.now())
    check_in = fields.Datetime('Date Check In', required=True,     
                                default = lambda self: fields.Datetime.now(),
                               
                                states={"draft": [("readonly", False)]})
    check_out = fields.Datetime('Date Check Out', required=True,
                                states={"draft": [("readonly", False)]})
    
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
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
            if record.number_of_guest == len(self.partner_ids) and record.number_of_guest <= self.room_id.capacity:
                record.state = 'check_in'
                record.room_id.state = 'occupied'
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

    def select_check_out(self):     

        self.state = 'check_out'
        self.room_id.state = 'available'

    def action_cancel(self):
         self.write({'state':'cancel'})

    @api.depends('invoice_id.payment_state')
    def _compute_payment_status(self):
        for rec in self:
            if rec.invoice_id.payment_state == 'paid':
                rec.payment_status = True
            else:
                rec.payment_status = False

    @api.depends('check_in', 'check_out', 'room_id.rent')
    def _compute_total_price(self):
        for rec in self:
            if rec.check_in and rec.check_out and rec.room_id.rent:
                days = (rec.check_out - rec.check_in).days
                rec.total_price = days * rec.room_id.rent

    @api.model
    def create(self, vals):         
        
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'reservation_sequence') or _('New')
        res = super().create(vals)
        return res

    @api.constrains('check_out')
    def check_as_check_out(self):
        for record in self:
            if record.check_out < record.check_in:
                raise ValidationError('The end date of the reservation must be greater than the start date')

                            