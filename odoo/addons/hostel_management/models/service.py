from odoo import models, fields

class Service(models.Model):
    _name = 'hostel.service'
    _description = 'Servicio del Hostal'


    service_type = fields.Selection([
        ('breakfast', 'Desayuno'),
        ('lunch', 'Almuerzo'),
        ('dinner', 'Cena'),
        ('wifi', 'Wi-Fi'),
        ('games', 'Área de Juegos'),
        ('pool', 'Piscina'),
         ('pmassage', 'Masaje'),
    ], 'Tipo de Servicio') 
   
    price = fields.Float('Precio')
