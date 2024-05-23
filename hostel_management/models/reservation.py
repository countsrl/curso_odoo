from datetime import datetime

from odoo import fields, models, api, _


class Reservations(models.Model):
    _name = 'reservation'

    sequence = fields.Char(string='Sequence')
    id_reservation = fields.Char('Reservation ID', default=lambda self: _('New'), readonly=True)
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
    states = fields.Selection(([('new', 'New'), ('confirm', 'Confirm'),
                                ('invoice', 'Invoice'), ('invoiced', 'Invoiced'), ('finished', 'Finished'),
                                ('canceled', 'Canceled')]), 'States', default='new')

    def action_cancelar(self):
        self.write({'states': 'canceled'})

    def name_get(self):
        result = []
        for record in self:
            name = record.id_reservation
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        request = super(Reservations, self).create(vals)

        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('reservation') or _('New')
            aux = 'R'
            date = datetime.now().year
            request.id_reservation = '{0}-{1}/{2}'.format(aux, vals['sequence'], date)

        request.write(vals)
        return request
