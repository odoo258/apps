# -*- coding: utf-8 -*-
from odoo import http

# class Testi1(http.Controller):
#     @http.route('/testi1/testi1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/testi1/testi1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('testi1.listing', {
#             'root': '/testi1/testi1',
#             'objects': http.request.env['testi1.testi1'].search([]),
#         })

#     @http.route('/testi1/testi1/objects/<model("testi1.testi1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('testi1.object', {
#             'object': obj
#         })