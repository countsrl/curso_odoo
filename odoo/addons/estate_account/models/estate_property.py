from odoo import models, fields, api, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # Llama al método original action_sold
        res = super(EstateProperty, self).action_sold()

        # Crea una factura con dos líneas de factura
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,  # El cliente
            'move_type': 'out_invoice',  # Factura de cliente
            'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,  # Diario de ventas
            'invoice_line_ids': [
                Command.create({
                    'name': '6% del precio de venta',  # Descripción de la línea
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,  # 6% del precio de venta de la propiedad
                    'account_id': self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_revenue').id)], limit=1).id,  # Cuenta de ingresos
                }),
                Command.create({
                    'name': 'Gastos administrativos',  # Descripción de la línea
                    'quantity': 1,
                    'price_unit': 100.00,  # Gastos administrativos
                    'account_id': self.env['account.account'].search([('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)], limit=1).id,  # Cuenta de gastos
                }),
            ],
        })

        # Confirma la factura
        invoice.action_post()

        return res