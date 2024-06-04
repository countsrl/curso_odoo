# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class RoomFloor(models.Model):
    _name = 'room.floor'
    _order = "name"
    _description = _('Room floor')
    _sql_constraints = [
       ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(_('Floor'), required=True)


    def unlink(self):
        if self.env.user.has_group("hostal_management.hostal_management_delete_record"):
            raise UserError("Not delete group")
        for rec in self:
            is_reservation_exist = self.env['rooms'].search([
                    ('floor_id', '=', rec.id),])           
            if is_reservation_exist:                  
                raise ValidationError(_("Floor %s is not available on delete") % (rec.name))
                
        
        return super().unlink()
   
   
    def write(self, vals):
      if 'name' in vals:
         raise ValidationError("No se puede modificar el nombre")
         
      return super(RoomFloor, self).write(vals)
