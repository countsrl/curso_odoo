# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _name = 'res.partner'
    _description = _('Res Partner')
    _inherit = "res.partner"

    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], string='Gender')
    reservation_id = fields.Many2one('hostal.reservation', string='Reservation')


class PartnerLine(models.Model):
    _name = 'hostal.partner.lines'
    _description = 'Hostal Partner Line'

    partner_id = fields.Many2one('res.partner',string='Name')
    reservation_id = fields.Many2one('hostal.reservation', string='Reservation')
    age = fields.Integer(string='Age', related='partner_id.age')
    gender = fields.Selection(related='partner_id.gender')
