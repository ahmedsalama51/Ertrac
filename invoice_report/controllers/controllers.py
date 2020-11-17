# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectErtrac(http.Controller):
#     @http.route('/project_ertrac/project_ertrac/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_ertrac/project_ertrac/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_ertrac.listing', {
#             'root': '/project_ertrac/project_ertrac',
#             'objects': http.request.env['project_ertrac.project_ertrac'].search([]),
#         })

#     @http.route('/project_ertrac/project_ertrac/objects/<model("project_ertrac.project_ertrac"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_ertrac.object', {
#             'object': obj
#         })
