# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'    
    
    _name = 'res.users'
    _description = 'User'

    property_ids = fields.One2many('estate.property', 'user_id', string='Properties')