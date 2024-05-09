# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class Estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = _('Estate property offer')
    _order = 'price desc'
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
        
    ]

    price = fields.Float('Price')
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"), 
            ("refused", "Refused ")
            
        ],
        string = "Status",        
        copy=False,
        default= False,
    )

    validity = fields.Integer("Validity (days)", default = 7)
    date_deadline = fields.Date("Deadline", compute= "_compute_date_deadline", inverse="_inverse_date_deadline")
    

    partner_id = fields.Many2one("res.partner",string = "Partner",required=True)
    property_id = fields.Many2one("estate.property", string= "Property", required=True)


    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env['estate.property'].browse(vals['property_id'])
            if prop.offer_ids:
                max_price = max(prop.offer_ids.mapped("price"))
                if float_compare(vals["price"], max_price, precision_rounding=0.01) <= 0 :
                    raise UserError("The offer must be higher than %.2f" % max_price)
            prop.write(
                {
                    "state":"offer_received",
                }
            )
                    
        
        return super().create(vals)


    def action_confirm(self):
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "status": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "status": "refused",
            }
        )

