from odoo import models, fields, api

class TechnicalOrderLine(models.Model):
    _name = 'technical.order.line'
    _description = 'Technical Order Line'

    _rec_name = 'description'
    _order = 'id ASC'

    technical_order_id = fields.Many2one(comodel_name="technical.order")
    product_id = fields.Many2one(comodel_name = 'product.product', string='Product')
    description = fields.Char(related='product_id.name')
    quantity = fields.Float(default=1)
    price = fields.Float(string='Price',related='product_id.lst_price')
    total = fields.Float(compute='_compute_total', string='Total')
    
    @api.depends('price','quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price * rec.quantity
    