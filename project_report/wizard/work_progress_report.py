# -*- coding: utf-8 -*-
import calendar
import logging

from odoo import fields, models, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)
YEARS = [(str(i), str(i)) for i in range(1990, 2100)]
REPORT_Type = [('report_1', "بيان موقف الأعمال"),
               ('report_2', "تقرير تقدم العمل بالتجديدات"),
               ('report_3', "أعمال الصيانه الصيفيه"),
               ('report_4', "أعمال تجديد أحواش المحطات"),
               ('report_5', "أعمال الصيانه الشتويه"),
               ('report_6', "إنتاج ماكينات الصيانه والتجديدات"),
               ('report_7', "مقارنه عن إنجازات الشركه المصريه")]
MONTHS = [('1', 'يناير'), ('2', 'فبراير'), ('3', 'مارس'), ('4', 'ابريل'),
          ('5', 'مايو'), ('6', 'يونيو'), ('7', 'يوليو'), ('8', 'اغسطس'),
          ('9', 'سبتمبر'), ('10', 'اكتوبر'), ('11', 'نوفمبر'), ('12', 'ديسمبر'), ]


class WorkProgressReportWizard(models.TransientModel):
    _name = 'work_progress_report'
    
    from_date = fields.Date(string='Date From')
    to_date = fields.Date(string='Date To')
    year = fields.Selection(YEARS, "Year", default='2020', required=True)
    year2 = fields.Selection(YEARS, "Year2", default='2019')
    month = fields.Selection(MONTHS, string='Month')
    report_type = fields.Selection(REPORT_Type, "Report Type", required=True, default='report_1')
    task_type_ids = fields.Many2many(comodel_name='ertrac.project.task.type', string="Task Types", required=1)
    
    @api.onchange('year', 'month')
    @api.depends('year', 'month')
    def _get_default_dates(self):
        if self.year or self.month:
            year = int(self.year) or fields.Date.today().year
            start_month = int(self.month) or 1
            end_month = int(self.month) or 12
            days = calendar.monthrange(year, end_month)
            self.from_date = fields.Date.today().replace(year=year, month=start_month, day=1)
            self.to_date = fields.Date.today().replace(year=year, month=end_month, day=days[1])
    
    def print_report(self):
        # TODO: remove when all types are done
        # if self.report_type in ['report_7']:
        #     raise Warning(_("Not yet done create this report, will be next phase ISA"))
        timesheets_obj = self.env['account.analytic.line']
        domain = [('task_id.task_type_id', 'in', self.task_type_ids.ids)]
        if self.from_date:
            domain.append(('date', '>=', self.from_date))
        if self.to_date:
            domain.append(('date', '<=', self.to_date))
        timesheets_ids = timesheets_obj.search(domain)
        datas = {
            'ids': timesheets_ids.ids,
            'model': 'account.analytic.line',
            'active_ids': timesheets_ids.ids,
            'date_from': self.from_date,
            'to_date': self.to_date,
            'task_type_ids': self.task_type_ids.ids,
            'report_type': self.report_type,
            'report_type_str': dict(self._fields['report_type'].selection).get(self.report_type),
            'month': self.month and dict(self._fields['month'].selection).get(self.month) or False,
            'year': self.year,
            'year2': self.year2,
        }
        return self.env.ref('project_report.timesheet_work_progress_report').report_action(timesheets_ids, data=datas)
