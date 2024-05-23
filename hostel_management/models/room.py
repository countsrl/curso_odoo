from datetime import datetime

from odoo import fields, models, api, _


class Room(models.Model):
    _name = 'room'

    sequence = fields.Char(string='Sequence')
    rooms_no = fields.Char('No Room', default=lambda self: _('New'), readonly=True)
    rooms_type = fields.Selection(
        [('private_B', 'Private room with bathroom'), ('private_cb', 'Private room with shared bathroom'),
         ('shared_b', 'Shared room with bathroom'), ('dormitory', 'Dormitory type room'), ('simple', 'Simple'),
         ('doble', 'Doble')])
    capacity = fields.Integer('Capacity', required=True)
    price = fields.Float('Price', required=True)
    states = fields.Selection(
        [('disponible', 'Disponible'), ('ocupada', 'Ocupada'), ('mantenimiento', 'En mantenimiento')], 'States',
        default='disponible')
    description = fields.Text('Description')
    floor = fields.Selection([('1', '1'), ('2', '2'), ('3', '3')], 'Floor', required=True)

    def name_get(self):
        result = []
        for record in self:
            name = record.rooms_no
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        request = super(Room, self).create(vals)

        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('room') or _('New')
            request.rooms_no = '{0}'.format(vals['sequence'])

        request.write(vals)
        return request
