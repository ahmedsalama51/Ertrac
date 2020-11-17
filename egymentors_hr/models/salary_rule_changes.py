# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class HRSalaryRuleParent(models.Model):
	_name = 'hr.salary.rule.parent'
	_description = "Salary Rule Parent"
	
	name = fields.Char("Rule Parent")
	
	
class HrSalayRuleInherit(models.Model):
	_inherit = 'hr.salary.rule'
	
	parent_id = fields.Many2one('hr.salary.rule.parent', "Parent")
	allowance = fields.Boolean("Allowance")
	deduction = fields.Boolean("Deduction")
	
	
class HrPayslipLineInherit(models.Model):
	_inherit = 'hr.payslip.line'
	
	allowance = fields.Boolean(related='salary_rule_id.allowance')
	deduction = fields.Boolean(related='salary_rule_id.deduction')
# Ahmed Salama Code End.
