from datetime import datetime

from odoo import fields, models, api, _


class Room(models.Model):
    _name = 'room'

    rooms_no = fields.Integer('No Rooms')
    rooms_type = fields.Selection(
        [('private_B', 'Private room with bathroom'), ('private_cb', 'Private room with shared bathroom'),
         ('shared_b', 'Shared room with bathroom'), ('dormitory', 'Dormitory type room')], required=True)
    # rooms_characteristics = fields.Many2many('room.characteristics', )
