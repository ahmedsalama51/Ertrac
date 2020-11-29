# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class LineType(models.Model):
	_name = 'line.type'
	
	name = fields.Char("Type")
	percentage = fields.Float("Percentage")
	discount = fields.Boolean("Discount?")
	tax = fields.Boolean("Tax?")


class SaleOrderLineInherit(models.Model):
	_inherit = 'sale.order.line'
	
	line_type_id = fields.Many2one('line.type', "Type", required=True)
	
	def _prepare_invoice_line(self):
		res = super(SaleOrderLineInherit, self)._prepare_invoice_line()
		if self.line_type_id:
			res['line_type_id'] = self.line_type_id.id
		return res


class InvoiceLineInherit(models.Model):
	_inherit = 'account.move.line'
	
	line_type_id = fields.Many2one('line.type', "Type", required=True)
	
# Ahmed Salama Code End.
