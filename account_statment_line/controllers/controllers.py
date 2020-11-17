# -*- coding: utf-8 -*-
from odoo import http

# class AccountStatmentLine(http.Controller):
#     @http.route('/account_statment_line/account_statment_line/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_statment_line/account_statment_line/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_statment_line.listing', {
#             'root': '/account_statment_line/account_statment_line',
#             'objects': http.request.env['account_statment_line.account_statment_line'].search([]),
#         })

#     @http.route('/account_statment_line/account_statment_line/objects/<model("account_statment_line.account_statment_line"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_statment_line.object', {
#             'object': obj
#         })