# -*- coding: utf-8 -*-
# from odoo import http


# class HrRules(http.Controller):
#     @http.route('/hr_rules/hr_rules/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_rules/hr_rules/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_rules.listing', {
#             'root': '/hr_rules/hr_rules',
#             'objects': http.request.env['hr_rules.hr_rules'].search([]),
#         })

#     @http.route('/hr_rules/hr_rules/objects/<model("hr_rules.hr_rules"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_rules.object', {
#             'object': obj
#         })
