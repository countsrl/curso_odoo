# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command

_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _inherit = 'estate.property'
    
    def action_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'partner_id': self.buyer_id.id,
                    'price_unit': self.selling_price * 0.06 + 100
                }),
            ],
        })
        return super().action_sold()