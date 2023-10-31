from odoo import fields, models, api

class TechnicalOrderWizard(models.TransientModel):
    _name = 'technical.order.wizard'
    _description = 'Technical Order Wizard'

    
    @api.model
    def default_get(self, fields):
        res = super(TechnicalOrderWizard, self).default_get(fields)
        res['technical_order_id'] = self.env.context['active_id']
        return res
        
    
    
    rejection_reason = fields.Text()
    
    technical_order_id= fields.Many2one('technical.order')
    
    def action_submit(self):
        self.technical_order_id.rejection_reason=self.rejection_reason
        self.technical_order_id.status='reject'

    
