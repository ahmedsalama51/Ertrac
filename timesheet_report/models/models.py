# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    line_type = fields.Selection([('increase_line','الخط الطالع'),('decrease_line','الخط النازل'),('odd_line','الخط المفرد')],string ='نوع الخط')
    from_km = fields.Float(string='From Km')
    to_km = fields.Float(string='To Km')
    total_km = fields.Float(string='Total Km', compute = '_compute_total_value')

    @api.onchange('from_km', 'to_km')
    @api.depends('total_km')
    def _compute_total_value(self):
        for line in self:
            line['total_km'] = line.to_km - line.from_km


class ProjectTaskInherit2(models.Model):
    _inherit = 'project.task'

#    def print_report(self):
#        task_ids = self.search().ids

#        return self.env.ref('report_timesheet_ertrac.task_ertrack2_report').report_action(task_ids)