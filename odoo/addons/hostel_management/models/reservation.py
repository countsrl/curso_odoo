from datetime import date, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Reservation(models.Model):
    _name = 'hostel.reservation'
    _description = 'Reserva del Hostal'
    
    reservation_id = fields.Char('#Reservation', copy=False) 
    
    # Basic fields
    num_persons = fields.Integer('Cantidad de Personas', required=True) 
    check_in_date = fields.Date('Fecha de Entrada', required=True)
    check_out_date = fields.Date('Fecha de Salida', required=True)
    state = fields.Selection([
        ('draft', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], 'Estado', default='draft')
    
    # Relations 
    guest_ids = fields.One2many('hostel.guest', 'reservation_id', string='Huéspedes')
    client_id = fields.Many2one('hostel.client', 'Cliente', required=True )
    room_id = fields.Many2one('hostel.room', 'Habitación', required=True)
    package_id = fields.Many2one('hostel.package', string='Paquete')
    
    # Computed fields 
    total_price = fields.Float(compute='_compute_total_price', store=True)
    days_until_check_in = fields.Integer(compute='_compute_days_until_check_in', store=True)
    days_since_check_out = fields.Integer(compute='_compute_days_since_check_out', store=True)
    is_room_available = fields.Boolean(compute='_compute_is_room_available', store=True)
    room_info = fields.Char(compute='_compute_room_info')

    @api.depends('check_in_date', 'check_out_date', 'room_id.price', 'package_id.price')
    def _compute_total_price(self):
       for reservation in self:
        if reservation.check_in_date and reservation.check_out_date and reservation.room_id:
            num_nights = (reservation.check_out_date - reservation.check_in_date).days
            if reservation.package_id:
                # Si hay un paquete seleccionado, añade su precio
                reservation.total_price = num_nights * reservation.room_id.price + reservation.package_id.price
            else:
                # Si no hay un paquete seleccionado, solo considera el precio de la habitación
                reservation.total_price = num_nights * reservation.room_id.price
        else:
            reservation.total_price = 0

    @api.depends('check_in_date')
    def _compute_days_until_check_in(self):
        for reservation in self:
            if reservation.check_in_date:
                delta = reservation.check_in_date - date.today()
                reservation.days_until_check_in = delta.days
            else:
                reservation.days_until_check_in = 0
    @api.depends('check_out_date')
    def _compute_days_since_check_out(self):
        for reservation in self:
            if reservation.check_out_date:
                delta = date.today() - reservation.check_out_date
                reservation.days_since_check_out = delta.days
            else:
                reservation.days_since_check_out = 0
    # function           
    def action_confirm(self):
     for record in self:
        if not record.reservation_id:
            record.reservation_id = self.env['ir.sequence'].next_by_code('hostel.reservation')
     self.write({'state': 'done'})
        
    def action_accept(self):
     self.state = 'confirmed'
    
    def action_refuse(self):
        self.state = 'cancelled'
  
    def action_cancel(self):
     for record in self:
        if record.state in ['draft', 'confirmed']:
            record.state = 'cancelled'
        else:
            raise UserError(_("No se puede cancelar la reserva porque ya ha sido procesada o cancelada."))
            
    @api.depends('room_id.is_available', 'check_in_date', 'check_out_date')
    def _compute_is_room_available(self):
     for reservation in self:
        if isinstance(reservation.id, int):  # Solo realiza la búsqueda si la reserva tiene un id asignado
            other_reservations = self.env['hostel.reservation'].search([
                ('room_id', '=', reservation.room_id.id),
                ('id', '!=', reservation.id),
                ('state', 'in', ['confirmed', 'done']),
                ('check_in_date', '<=', reservation.check_out_date),
                ('check_out_date', '>=', reservation.check_in_date)
            ])
            reservation.is_room_available = reservation.room_id.is_available and len(other_reservations) == 0
        else:
            reservation.is_room_available = reservation.room_id.is_available

    @api.model
    def create(self, vals):
        room = self.env['hostel.room'].browse(vals.get('room_id'))
        if not room.is_available:
            raise UserError("La habitación seleccionada no está disponible.")
        return super().create(vals)

    def write(self, vals):
        if 'room_id' in vals:
            room = self.env['hostel.room'].browse(vals.get('room_id'))
            if not room.is_available:
                raise UserError("La habitación seleccionada no está disponible.")
        return super().write(vals)
    @api.depends('room_id')
    def _compute_room_info(self):
        for reservation in self:
            if reservation.room_id:
                room = reservation.room_id
                info = f'Número: {room.number}, Tipo: {room.room_type}, Capacidad: {room.capacity}, # Camas: {room.num_beds}, Ac: {room.has_ac}, Terraza: {room.has_terrace}, # Baños: {room.num_bathrooms}, Precio *Noche: {room.price}'  
                reservation.room_info = info
            else:
                reservation.room_info = ''