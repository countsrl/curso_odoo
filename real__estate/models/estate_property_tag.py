# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = _('Estate_property_tag')

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists!")]
