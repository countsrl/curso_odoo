from odoo import fields, models, api
from odoo.fields import Command


class Property(models.Model):
    _inherit = 'estate.property'

    def action_vender(self):
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({'name': self.name,
                                'quantity': 1,
                                'partner_id': self.buyer.id,
                                'price_unit': self.sale_price * 0.06 + 100}),
            ],
        })

        return super().action_vender()
