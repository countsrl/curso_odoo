# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class Estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = _('property_type')

    name = fields.Char(_('Name', required=True))
