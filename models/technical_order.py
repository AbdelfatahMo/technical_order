# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TechnicalOrder(models.Model):
    _name = 'technical.order'
    _description = 'technical_order'

    sequence = fields.Char(readonly=True)

    request_name = fields.Char(required=True)
    request_by = fields.Many2one(
        comodel_name="res.users", required=True, default=lambda self: self.env.user)

    customer = fields.Many2one(comodel_name="res.partner", required=True, domain=[
                               ('is_tech_offer', '=', True)])
    is_tech_offer = fields.Boolean()
    start_date = fields.Date(default=lambda self: fields.date.today())
    end_date = fields.Date()

    rejection_reason = fields.Text(readonly=1)

    status = fields.Selection(selection=[('draft', 'Draft'), ('to_be_approved', 'To be Approved'),
                                         ('approve', 'Approve'), ('reject', 'Reject'),
                                         ('cancel', 'Cancel')], readonly=True,default="draft")

    technical_order_line_ids = fields.One2many(
        'technical.order.line', 'technical_order_id', string='Technical Order Line')

    total_price = fields.Float(compute="_total_price_compute")
    
    sales_order_ids = fields.One2many('sale.order','technical_order_id')
    
    sales_order_count = fields.Integer(compute="_sales_order_compute")

    @api.depends('sales_order_ids')
    def _sales_order_compute(self):
        for record in self:
            count = 0
            for rec in record.sales_order_ids:
                count += 1
            record.sales_order_count = count
    
    
    @api.depends('technical_order_line_ids')
    def _total_price_compute(self):
        for record in self:
            total = 0
            for line in record.technical_order_line_ids:
                total += line.total
            record.total_price = total

    def action_cancel(self):
        for rec in self:
            rec.status = "cancel"

    def action_submit_for_approve(self):
        for rec in self:
            rec.status = "to_be_approved"
    
    def action_approve(self):
        manager_users = self.env.ref('technical_order.group_manager').users
        template = self.env.ref('technical_order.email_technical_order_manager_appprove')
        for user in manager_users:
            template.send_mail(self.id, force_send=True, email_values={'email_to': user.email})
        self.status = "approve"

    def action_reject(self):
        return {
            'name': 'Rejection Reason',
            'res_model': 'technical.order.wizard',
            'view_mode': 'form',
            'context': {'default_technical_order_id': self.id},
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
    def view_sale_order(self):
        return {
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain':[('technical_order_id','=',self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }
        

    def action_reset_to_draft(self):
        for record in self:
            record.status = 'draft'
            record.rejection_reason = None
    
    def action_create_os(self):
        for record in self:
            sale_order = self.env['sale.order'].create({
                'technical_order_id': record.id,
                'partner_id': record.customer.id,
                'state': 'draft',
                # 'pricelist_id' : self.env.company.property_product_pricelist.id
            })
            for rec in record.technical_order_line_ids:
                self.env['sale.order.line'].create({
                    'order_id' : sale_order.id,
                    'product_id' : rec.product_id.id,
                    'name' : rec.description,
                    'product_uom_qty' : rec.quantity
                })
            

    @api.model
    def create(self, values):
        values['sequence'] = self.env["ir.sequence"].next_by_code("technical.order")
        return super(TechnicalOrder,self).create(values)
