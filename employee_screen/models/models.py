# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class hrScreen(models.Model):
    
    _name = "hr.screen"
    _inherit = ['mail.thread']

    month = fields.Selection([('january','January'),('february','February'),('march','March'),
                              ('april', 'April'),('may', 'May'), ('june', 'June'), ('july', 'July'),
                              ('august', 'August'),('september', 'September'),
                              ('october', 'October'), ('november', 'November'), ('december', 'December')],
                             string='Month')
    ### if it didnot work use .strftime("%B") instead of .month()
    external_employee = fields.Many2many('external.employee', string="Ext. Employee")
    date = fields.Date(string="Date",default=datetime.today())

    amount_total = fields.Float(string="Total Amount", compute="_cal_total_amount")
    net_total = fields.Float(string="Total Net", compute="_cal_total_net")

    @api.depends('external_employee.amount')
    def _cal_total_amount(self):
        total = 0
        for emp in self.external_employee:
            total = emp.amount + total
        self.amount_total = total

    @api.depends('external_employee.net')
    def _cal_total_net(self):
        total = 0
        for emp in self.external_employee:
            total = emp.net + total
        self.net_total = total
    
    
class ExternalEmployee(models.Model):
    _name = 'external.employee'

    employee_name = fields.Char(string="Name")
    department = fields.Char(string="Department", required=True)
    job_position_ex = fields.Char(string="Job Position")
    amount = fields.Float(string="Amount", store=True)
    tax = fields.Float(string="Tax", default=0.10, store=True, readonly=True)
    net = fields.Float(string="NET", store=True, compute='_compute_net_amount')
    notes = fields.Char(string="Notes")

    @api.depends('amount', 'tax')
    def _compute_net_amount(self):
        self.net = (self.amount - (self.amount * self.tax))

    @api.onchange('amount')
    def _on_change_amount(self):
        self.net = (self.amount - (self.amount * self.tax))


