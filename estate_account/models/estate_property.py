# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _name = 'estate.property'
    _description = _('Estate_property')
    _inherit = "estate.property"

    name = fields.Char(_('Name'))

    def action_sold(self):
        return super().action_sold()
        