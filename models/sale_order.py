from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    technical_order_id = fields.Many2one(
        'technical.order',
        string='Technical Order',
        )
    
    def action_view_quotation(self):
        return {
            'name':_('Technical Order'),
            'res_model':'technical.order',
            'view_mode':'list,form',
            'domain':[('id','=',self.technical_order_id.id)],
            'target':'new',
            'type':'ir.actions.act_window'
        }
        
    def action_confirm(self):
        super().action_confirm()
        tech_order_SOs= self.env['sale.order'].search([('technical_order_id','=',self.technical_order_id)])
        for order in tech_order_SOs:
            if order.state == 'sale':
                pass 
    
        

    @api.constrains('order_line')
    def _check_order_line(self):
        tech_lines = [line for line in self.technical_order_id.technical_order_line_ids]
        for line in self.order_line:
            for tech_line in tech_lines:
                if line.product_id.id == tech_line.product_id.id:
                    if line.product_uom_qty > tech_line.quantity:
                        raise ValidationError(f"Quantity of {line.product_id.name} is more than Required")
            
    