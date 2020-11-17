# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeScreen(http.Controller):
#     @http.route('/employee_screen/employee_screen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_screen/employee_screen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_screen.listing', {
#             'root': '/employee_screen/employee_screen',
#             'objects': http.request.env['employee_screen.employee_screen'].search([]),
#         })

#     @http.route('/employee_screen/employee_screen/objects/<model("employee_screen.employee_screen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_screen.object', {
#             'object': obj
#         })
