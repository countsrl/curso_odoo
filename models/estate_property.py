# -*- coding: utf-8 -*-
import logging

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _name = 'estate.property'
    _description = _('Properties')

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    name = fields.Char(_('Title'), required=True)
    description = fields.Text("Description")    
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default= lambda self: self._default_date_availability())
    expected_price = fields.Float("Expected Price", required=True, copy=False)
    selling_price = fields.Float("Selling Price", readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2 )
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden") 
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        selection=[
            ("N", "North"), 
            ("S", "South"),
            ("E", "East"),
            ("W", "West"),
        ],
        string = "Garden Orientation",
    )
    active = fields.Boolean('Active', default= True)
    state = fields.Selection(
        selection=[
            ("new", "New"), 
            ("offer_received", "Offer Received "),
            ("offer_accepted", "Offer Accepted "),
            ("sold", "Sold "),
            ("cancel", "Cancelled")
        ],
        string = "Status",
        required=True,
        copy=False,
        default= "new",
    )


    total_area = fields.Integer(
        "Total area (sqm)",
        compute= "_compute_total_area")
    

    property_type_id = fields.Many2one("estate.property.type",string = "Property Type")
    user_id = fields.Many2one("res.users",string = "Salesman", default= lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner",string = "Buyer",copy=False, readonly=True)
    tag_ids = fields.Many2many("estate.property.tag", string= "Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id", string= "Offer")
    


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = ""


    
    
    
