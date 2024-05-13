from unittest import result
from odoo import models, fields, api, Command
from odoo.exceptions import UserError
#import debugpy

# Allow other computers to attach to debugpy at this IP address and port.
#debugpy.listen(('0.0.0.0', 5678))

# Pause the program until a remote debugger is attached
#debugpy.wait_for_client()

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    # Define un método para crear una factura
    def _create_invoice(self, partner, lines):
        # Establece el tipo de movimiento para la factura
        move_type = 'out_invoice'
        # Obtiene el diario predeterminado para este tipo de movimiento
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()

        try:
            # Intenta crear la factura
            invoice = self.env['account.move'].create({
                'partner_id': partner.id,
                'move_type': move_type,
                'journal_id': journal.id,
                'invoice_date': fields.Date.today(),  # fecha de la factura
                'invoice_line_ids': lines,
            })
            # Publica la factura
            invoice.action_post()
            return invoice
        except Exception as e:
            raise UserError(f"Error creating invoice: {e}")
    # Sobrescribe el método 'action_sold'
    def action_sold(self):
        result = super().action_sold()
        # Itera sobre cada registro en el conjunto de registros
        for prop in self:
            if prop.state != 'offer_accepted':
                raise UserError("Only properties with 'Offer Accepted' state can be sold.")
            # Obtiene el comprador de la propiedad
            partner = prop.buyer_id
            if not partner:
                raise UserError("A buyer must be set before selling a property.")
            # Define las líneas de factura
            invoice_lines = [
                Command.create({
                    'name': 'Property Commission',
                    'quantity': 1,
                    'price_unit': prop.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ]
            # Crea la factura
            invoice = self._create_invoice(partner, invoice_lines)
           

        return result