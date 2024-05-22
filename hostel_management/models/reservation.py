from datetime import datetime

from odoo import fields, models, api, _


class Reservations(models.Model):
    _name = 'reservation'

    id_reservation = fields.Char('Reservation ID', required=True)
    client_id = fields.Many2one('res.partner', 'Client name', reuired=True)
    room_no = fields.Integer('Room No.', required=True)
    init_date = fields.Date('Init Date', required=True)
    end_date = fields.Date('End Date', required=True)
    number_nights = fields.Integer('Number of nights', required=True)
    total_price = fields.Float('Total Price', required=True)
    method_payment = fields.Selection(([('online_payment', 'Online Payment'), ('check', 'Check'), ('cash', 'Cash')]),
                                      'Method of Payment', required=True)
    notes = fields.Text('Notes')
    service_ids = fields.Many2many('service')
    states = fields.Selection(
        ([('confirm', 'Confirm'), ('canceled', 'Canceled'), ('new', 'New'), ('finished', 'Finished')]), 'States',
        default='new')

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