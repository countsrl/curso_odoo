from unittest import result
from odoo import models, fields, api, Command
from odoo.exceptions import UserError
#import debugpy
import logging
_logger = logging.getLogger(__name__)
# Allow other computers to attach to debugpy at this IP address and port.
#debugpy.listen(('0.0.0.0', 5678))

# Pause the program until a remote debugger is attached
#debugpy.wait_for_client()

class EstatePropertyInherit(models.Model):
    _inherit = 'estate.property'
    # Define un método para crear una factura
    def _create_invoice(self, partner, lines):
        # Establece el tipo de movimiento para la factura
        move_type = 'out_invoice'
        # Obtiene el diario predeterminado para este tipo de movimiento
        journal = self.env['account.move'].with_context(default_move_type=move_type)._get_default_journal()
        _logger.debug(f"Diario predeterminado obtenido: {journal.id}")
        try:
            # Intenta crear la factura
            invoice = self.env['account.move'].create({
                'partner_id': partner.id,
                'move_type': move_type,
                'journal_id': journal.id,
                'invoice_date': fields.Date.today(),  # fecha de la factura
                'invoice_line_ids': lines,
            })
            _logger.debug(f"Factura creada con ID: {invoice.id}")
            # Publica la factura
            invoice.action_post()
            _logger.debug(f"Factura publicada con ID: {invoice.id}")
            return invoice
        except Exception as e:
            _logger.error(f"Error al crear la factura: {e}")
            raise UserError(f"Error creating invoice: {e}")
    # Sobrescribe el método 'action_sold'
    def action_sold(self):
        _logger.debug(f"Estado de la propiedad antes de vender: {self.state}")
        result = super(EstatePropertyInherit, self).action_sold()
        _logger.debug(f"Resultado de super().action_sold(): {result}")
        # Itera sobre cada registro en el conjunto de registros
        for prop in self:
            if prop.state != 'offer_accepted':
                raise UserError("Only properties with 'Offer Accepted' state can be sold.")
            _logger.debug(f"Estado de la propiedad verificado: {prop.state}")
            # Obtiene el comprador de la propiedad
            partner = prop.buyer_id
            if not partner:
                raise UserError("A buyer must be set before selling a property.")
            _logger.debug(f"Creando factura para la propiedad: {prop.name}")
            if prop.selling_price <= 0:
                raise UserError("El precio de venta debe ser mayor que cero.")
            if prop.selling_price * 0.06 <= 0:
                raise UserError("La comisión calculada debe ser mayor que cero.")
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
            _logger.debug(f"Líneas de factura creadas: {invoice_lines}")
            # Crea la factura
            invoice = self._create_invoice(partner, invoice_lines)
            _logger.debug(f"Factura creada con ID: {invoice.id}")
            # Cambia el estado a 'sold' después de crear la factura
            prop.state = 'sold'
            _logger.debug(f"Estado de la propiedad después de vender: {prop.state}")
        return result