# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = _('Property tags')

    name = fields.Char(_('Name'), required=True)
