from odoo import fields, models, api


class Property(models.Model):
    _inherit = 'estate.property'

    def action_vender(self):
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
        })

        self.env['account.move.line'].create({
            'move_id': invoice.id,
            'name': self.name,
            'quantity': 1,
            'price_unit': self.sale_price * 0.06 + 100,
        })

        return super().action_vender()
