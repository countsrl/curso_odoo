# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import models, Command

_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _name = 'estate.property'
    _description = _('Estate_property')
    _inherit = "estate.property"

    name = fields.Char(_('Name'))

    def action_sold(self):
        res = super().action_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for rec in self:
            self.env["account.move"].create(
                {
                    "partner_id": rec.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({
                            "name": rec.name,
                            "quantity": 1.0,
                            "price_unit": rec.selling_price * 6.0 / 100.0,
                        }),
                        Command.create({
                            "name": "Administrative",
                            "quantity": 1.0,
                            "price_unit": 100.0,
                        }),
                    ],
                }
            )
        return res
        