from odoo import fields, models, api, _


class HostelManagement(models.Model):
    _name = 'hostel.management'

    name = fields.Char('Area Name', required=True)
    prepared_by = fields.Char('Prepared by', required=True)
    init_date = fields.Date('Init Date', required=True)
    end_date = fields.Date('End Date', required=True)
    states = fields.Selection([('draft', 'Draft'),
                               ('required', 'Required'),
                               ('accounted', 'Accounted')], default='draft')
    order_date = fields.Date('Order Date')

    def go_return(self):
        if self.states == 'required':
            self.write({'states': 'draft'})

    def go_accounted(self):
        return
