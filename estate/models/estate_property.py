from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    # Constrains sql
    _sql_constraints = [('check_price_exp', 'CHECK(price_exp > 0)',
                         'El precio esperado de una propiedad debe ser estrictamente positivo'),
                        ('check_sale_price', 'CHECK(sale_price >= 0)',
                         'El precio de venta de una propiedad debe ser positivo')]
    _order = "id desc"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date = fields.Date('Available From', copy=False,
                       default=lambda self: fields.Date.context_today(self).replace(day=1, month=9, year=2023), )
    price_exp = fields.Float('Expected Price', required=True)
    sale_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'), ('oeste', 'Oeste')],
                                          'Garden Orientation')
    state = fields.Selection([('nuevo', 'Nuevo'), ('oferta_rec', 'Oferta Recibida'), ('oferta_acep', 'Oferta Aceptada'),
                              ('vendido', 'Vendido'), ('cancelado', 'Cancelado')], 'Status', required=True, copy=False,
                             default='nuevo')
    property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    salesman = fields.Many2one('res.users', 'Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', 'Buyer', copy=False)
    tags_ids = fields.Many2many('estate.property.tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
    best_price = fields.Float('Best Offer', compute='_compute_best_price', store=True)

    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
    active = fields.Boolean('Active', default=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    # Este codigo imprime el valor maximo almacenado en un campo usando la funcion mapped para listar sus valores
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        best_price = max(self.mapped('offer_ids.price'), default=0)
        self.best_price = best_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'norte'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancelar(self):
        if self.state == 'vendido':
            # Uso de exepciones para mostrar mensajes
            raise ValidationError('El registro no puede ser cancelado.')
        else:
            # Asignarle valor a un campo a traves de un boton
            self.write({'state': 'cancelado'})
            self.state = 'cancelado'

        return True

    def action_vender(self):
        if self.state == 'cancelado':
            raise ValidationError('El registro no puede ser vendido.')
        else:
            self.write({'state': 'vendido'})
            self.state = 'vendido'

        return True

    # Constrains python
    @api.constrains('price_exp', 'sale_price')
    # Funcion para comparar valores
    def check_sale_price(self):
        for rec in self:
            if rec.price_exp and rec.sale_price < rec.price_exp * 0.9:
                if not (float_compare(rec.sale_price, 0.0,
                                      precision_digits=rec.currency_id.decimal_places) == 0 or float_is_zero(
                    rec.price_exp, precision_digits=rec.currency_id.decimal_places)):
                    raise ValidationError('El precio de venta no puede ser inferior al 90% del precio esperado')
