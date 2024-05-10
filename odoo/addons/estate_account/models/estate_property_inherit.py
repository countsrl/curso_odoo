from odoo import models, fields

class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    def action_sold(self):
        # Crear la factura
        invoice = self.env['account.move'].create({
            'type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Venta de propiedad',
                'quantity': 1,
                'price_unit': self.selling_price,
            })],
        })
        # Asignar la factura al campo invoice_id
        self.invoice_id = invoice.id
        return super().action_sold()