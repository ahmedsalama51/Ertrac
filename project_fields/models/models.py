# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class project_fields(models.Model):
#     _name = 'project_fields.project_fields'
#     _description = 'project_fields.project_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class AccountAnalyticLineInherit(models.Model):
    _inherit = 'account.analytic.line'

    region = fields.Selection([('normal', 'عادديه'), ('remote', 'نائيه')], "نوع المنطقه")
    work_type = fields.Selection([('branching', 'تفريعه'), ('path', 'سكه'), ('keys', 'مفتاح')], "نوع العمل")
    description2 = fields.Char(string="Description2")
    
    # Allowing up to 4 decimal places in Line Quantity
    unit_amount = fields.Float('Quantity', digits=(12, 4))
