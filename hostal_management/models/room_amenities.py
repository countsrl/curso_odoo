# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Room_amenities(models.Model):
    _name = 'room.amenities'
    _order = 'sequence, name'
    _description = _('Room amenities')
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
        
    ]

    name = fields.Char(_('Amenities'), required=True)
    sequence = fields.Integer("Sequence", default=10)


    def unlink(self):
        if self.env.user.has_group("hostal_management.hostal_management_delete_record"):
            raise UserError("Not delete group")
        for rec in self:
            is_reservation_exist = self.env['rooms'].search([
                    ('room_amenities_ids', '=', rec.id),])           
            if is_reservation_exist:                  
                raise ValidationError(_("Room amenities %s is not available on delete") % (rec.name))
                
        
        return super().unlink()

    def write(self, vals):
      if 'name' in vals:
         raise ValidationError("No se puede modificar el nombre")
         
      return super(Room_amenities, self).write(vals)