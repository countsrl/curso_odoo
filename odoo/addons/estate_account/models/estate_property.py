from odoo import models, fields, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Crear una factura vacía
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
        })

        # Agregar líneas de factura
        invoice_line_vals = [
            Command.create({
                'name': 'Venta de propiedad',
                'quantity': 1,
                'price_unit': self.selling_price * 0.06,
            }),
            Command.create({
                'name': 'Gastos administrativos',
                'quantity': 1,
                'price_unit': 100.00,
            }),
        ]

        invoice.write({'invoice_line_ids': invoice_line_vals})

        return super().action_sold()