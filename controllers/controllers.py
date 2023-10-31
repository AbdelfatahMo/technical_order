# -*- coding: utf-8 -*-
# from odoo import http


# class TechnicalOrder(http.Controller):
#     @http.route('/technical_order/technical_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/technical_order/technical_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('technical_order.listing', {
#             'root': '/technical_order/technical_order',
#             'objects': http.request.env['technical_order.technical_order'].search([]),
#         })

#     @http.route('/technical_order/technical_order/objects/<model("technical_order.technical_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('technical_order.object', {
#             'object': obj
#         })
