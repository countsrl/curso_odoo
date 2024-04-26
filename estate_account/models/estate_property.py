from odoo import fields, models, api
from odoo import Command


class Property(models.Model):
    _inherit = 'estate.property'

    def action_vender(self):
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'lines_id': [Command.create({
                "field_1": "value_1",
                "field_2": "value_2",

            })]

        })
        return super().action_vender()


