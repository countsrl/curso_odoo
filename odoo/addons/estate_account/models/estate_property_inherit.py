from odoo import models, fields, Command

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"


    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    def action_sold(self):
        # Llama al método original
        result = super().action_sold()

        # Crea una factura
        invoice = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',  # Factura de cliente
            'invoice_date': fields.Date.today(),
            'journal_id': 1,
            'invoice_line_ids': [
                Command.create({
                    'name': 'Venta de propiedad',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,  # 6% del precio de venta
                }),
                Command.create({
                    'name': 'Gastos administrativos',
                    'quantity': 1,
                    'price_unit': 100.00,  # Gastos administrativos
                })
            ],
        })

        # Confirma la factura
        invoice.action_post()

        # Asigna la factura a la propiedad
        if invoice.exists():
            self.invoice_id = invoice.id
        else:
            self.invoice_id = None

        return result
