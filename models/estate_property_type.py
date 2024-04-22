# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = _('Property Type')

    name = fields.Char(_('Property Type'), required=True)
