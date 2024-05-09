# -*- coding: utf-8 -*-
import logging

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class Estate_property(models.Model):
    _name = 'estate.property'
    _description = _('Properties')
    _order = 'id desc'
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]
    
    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    name = fields.Char(_('Title'), required=True)
    description = fields.Text("Description")    
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default= lambda self: self._default_date_availability())
    expected_price = fields.Float("Expected Price", required=True)
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
        readonly=True,
    )


    total_area = fields.Integer(
        "Total area (sqm)",
        compute= "_compute_total_area")
    

    best_price = fields.Float(
        "Best offer",
        compute= "_compute_best_price",
        store=True)
    

    property_type_id = fields.Many2one("estate.property.type",string = "Property Type")
    user_id = fields.Many2one("res.users",string = "Salesman", default= lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner",string = "Buyer",copy=False, readonly=True)
    tag_ids = fields.Many2many("estate.property.tag", string= "Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id", string= "Offer")
    

    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for rec in self:
            if (not float_is_zero(rec.selling_price, precision_rounding=0.01)
                and float_compare(rec.selling_price, rec.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0 ):

                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )




    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            best_price = max(rec.offer_ids.mapped("price"),default=0.0)
            rec.best_price = best_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
 
    
    
    def unlink(self):
        for rec in self:
            if(rec.state != "new" and rec.state != "cancel"):
                raise UserError('Only new and canceled properties can be deleted.')
            
        return super().unlink()
    




    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError('Canceled properties cannot be sold')
            else:
                record.state = "cancel"         

        return True
    
    def action_sold(self):
        for record in self:
            if record.state == "cancel":
                raise UserError('Canceled properties cannot be sold')
            else:
                record.state = "sold"         

        return True


    
    
    
