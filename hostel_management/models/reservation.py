from datetime import datetime

from odoo import fields, models, api, _


class Reservations(models.Model):
    _name = 'reservation'

    no_reservation = fields.Char('Reservation No', required=True)
    # room_type = fields.Selection('Room Type', required=True)
    init_date = fields.Date('Init Date', required=True)
    end_date = fields.Date('End Date', required=True)
    # services = fields.Many2many()
    # services_plus = fields.Many2many()
    # states = fields.Selection()

    @api.model
    def create(self, vals):
        request = super(Reservations, self).create(vals)
        if vals.get('sequence', _('New')) == _('New'):
            # Generar un número de solicitud único
            vals['sequence'] = self.env['ir.sequence'].next_by_code('reservation') or _('New')
            aux = 'R'
            date = datetime.now().year
            request.no_reservation = '{0}-{1}/{2}'.format(aux, vals['sequence'], date)
        return super(Reservations, self).write(vals)
