# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Rooms(models.Model):
    _name = 'rooms'
    _order = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    _description = _('Rooms')
    _sql_constraints = [
        ("check_capacity", "CHECK(capacity > 0)", "The capacity must be strictly positive"),
        ("check_rent", "CHECK(rent > 0)", "The rent must be strictly positive"),
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(_('Room Number'), required=True)    
    color = fields.Integer('Color')
    active = fields.Boolean(string=_('Active'), default=True)
    capacity = fields.Integer('Capacity', required=True, default=1)
    state = fields.Selection(
        selection=
            [("available", "Available"), 
            ('maintenance', 'Maintenance'),
            ("occupied", "Occupied")], 
        default='available',            
        string="Status"
    )
    bed = fields.Selection(
        selection=[
            ("single", "Single"),
            ("double", "Double"),
            ("dormitory", "Dormitory")
           
        ],
        string="Bed",
    )
    available_beds = fields.Integer('Available Beds')
    rent = fields.Monetary('Rent (per day)',required=True)
    currency_id = fields.Many2one('res.currency', readonly=True,
                                    default=lambda self: self.env.company.currency_id)
    
    # is_available_check = fields.Boolean(string=_('Available Check'), compute='_compute_is_available',
    #                                 store=True, default=False)
    
    room_amenities_ids = fields.Many2many('room.amenities', string='Room Amenities')
    floor_id = fields.Many2one('room.floor', string='Floor No', ondelete="restrict")
    reservation_count = fields.Integer(
        string='Reservation count',
        compute='_compute_reservation_count',
    )
    reservation_ids = fields.One2many('hostal.reservation', 'room_ids', string='Reservation')
    
    
    @api.depends('reservation_ids')
    def _compute_reservation_count(self):
        for record in self:
            record.reservation_count = len(record.reservation_ids)
    

    # hostal_reservation_ids = fields.One2many('hostal.reservation', 'room_id', string='Hostal Reservation')
      

    def action_maintenance(self):                      
        self.state = 'maintenance'

    def action_available(self):                      
        self.state = 'available'

    


    def set_room_status_occupied(self):
        
        return self.write({"color": 2})

    def set_room_status_available(self):
        
        return self.write({"color": 5})

    def unlink(self):
        if self.env.user.has_group("hostal_management.hostal_management_delete_record"):
            raise UserError("Not delete group")
        for rec in self:
            is_reservation_exist = self.env['hostal.reservation'].search([
                    ('room_ids', '=', rec.id),])           
            if is_reservation_exist:                  
                raise ValidationError(_("Room %s is not available on delete") % (rec.name))
                
        
        return super().unlink()

    def write(self, vals):
      if 'name' in vals:
         raise ValidationError("No se puede modificar el nombre")
         
      return super(Rooms, self).write(vals)


    def action_view_reservation(self):
        
        res_action = {
            'name': _(' Reservation Rooms'),
            'type': 'ir.actions.act_window',            
            'res_model': 'hostal.reservation',
            'target' : 'current' ,            
        }

        reservations = self.reservation_ids.ids
        if len(reservations) == 1:
            res_action['res_id'] = reservations[0]
            res_action['view_mode'] = 'form'
        else:
            res_action['view_mode'] = 'tree,form'
            res_action['domain'] = [('id', 'in', reservations)]
        return res_action

        
