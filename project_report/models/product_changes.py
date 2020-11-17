# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class ProductTemplateInherit(models.Model):
	_inherit = 'product.template'
	
	task_type_id = fields.Many2one('ertrac.project.task.type', "Task Type")


class ProjectTaskType(models.Model):
	_name = 'ertrac.project.task.type'
	_description = "Project Task Type"
	
	name = fields.Char("Type", required=True)
	code = fields.Char("Code")
	
	_sql_constraints = [('code_unique', 'unique(code)', _('Type Code should be unique!'))]
# Ahmed Salama Code End.
