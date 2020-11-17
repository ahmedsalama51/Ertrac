# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountStatmentLine(models.Model):
    _inherit = 'account.bank.statement.line'

    statment_type = fields.Selection([
        ('Mangment', 'management'),
        ('Salary', 'salary'),
        ('Organization', 'orgnization'),
        ('Invoices', 'invoices'),
        ('Adding', 'adding'),
    ], string='Type')

    doc_no = fields.Monetary(string='Doc No')
    