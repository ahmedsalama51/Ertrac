# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


# Ahmed Salama Code Start ---->

class SaleOrderLineInherit(models.Model):
	_inherit = 'sale.order.line'
	
	task_type_id = fields.Many2one(related='product_id.task_type_id')
	region = fields.Selection([('normal', 'عادديه'), ('remote', 'نائيه')], "نوع المنطقه")
	season_type = fields.Selection([('summer', 'صيفي'), ('winter', 'شتوي')], "الموسم")
	work_type = fields.Selection([('branching', 'تفريعه'), ('path', 'سكه'), ('keys', 'مفتاح')], "نوع العمل")
	
	def _timesheet_create_task_prepare_values(self, project):
		vals = super(SaleOrderLineInherit, self)._timesheet_create_task_prepare_values(project)
		vals['task_type_id'] = self.task_type_id and self.task_type_id.id or False
		vals['season_type'] = self.season_type
		return vals


class AccountAnalyticLineInherit(models.Model):
	_inherit = 'account.analytic.line'
	
	task_type_id = fields.Many2one('ertrac.project.task.type', "Task Type")
	region = fields.Selection([('normal', 'عادديه'), ('remote', 'نائيه')], "نوع المنطقه")
	work_type = fields.Selection(related='so_line.work_type')
	season_type = fields.Selection(related='so_line.season_type')
	
# Ahmed Salama Code End.
