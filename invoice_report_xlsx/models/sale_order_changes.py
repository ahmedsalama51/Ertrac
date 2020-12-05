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
	
	line_type_id = fields.Many2one('line.type', "Type")
	
	def _prepare_invoice_line(self):
		res = super(SaleOrderLineInherit, self)._prepare_invoice_line()
		if self.line_type_id:
			res['line_type_id'] = self.line_type_id.id
		return res
	
	def get_line_amount(self):
		print('------------------in ---------------')
		for line in self:
			if line.line_type_id and \
					(line.line_type_id.discount or line.line_type_id.tax) and line.line_type_id.percentage:
				print("all: ", line.order_id.order_line.mapped('line_type_id.name'))
				other_lines = line.order_id.order_line.\
					filtered(lambda l: not l.line_type_id or (l.line_type_id and not l.line_type_id.discount and not l.line_type_id.tax))
				print("OTHER: ", other_lines.mapped('product_id.name'))
				# other_lines._compute_amount()
				if other_lines:
					line.product_uom_qty = 1
					lines_amount = sum(ln.product_uom_qty * ln.price_unit for ln in other_lines)
					print("lines_amount: ", lines_amount)
					line_amount = lines_amount * line.line_type_id.percentage / 100
					print("line_amount: ", line_amount)
					if line.line_type_id.discount:
						line.price_unit = -line_amount
					elif line.line_type_id.tax:
						line.price_unit = line_amount


class InvoiceLineInherit(models.Model):
	_inherit = 'account.move.line'
	
	line_type_id = fields.Many2one('line.type', "Type", required=True)

# Ahmed Salama Code End.
