# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Rooms(models.Model):
    _name = 'rooms'
    _order = "name"
    _description = _('Rooms')
    _sql_constraints = [
        ("check_capacity", "CHECK(capacity > 0)", "The capacity must be strictly positive"),
        ("check_rent", "CHECK(rent > 0)", "The rent must be strictly positive"),
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(_('Room Number'), required=True)    
    color = fields.Integer('Color')
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

    # hostal_reservation_ids = fields.One2many('hostal.reservation', 'room_id', string='Hostal Reservation')
      

    def action_maintenance(self):                      
        self.state = 'maintenance'

    def action_available(self):                      
        self.state = 'available'

    


    def set_room_status_occupied(self):
        
        return self.write({"color": 2})

    def set_room_status_available(self):
        
        return self.write({"color": 5})