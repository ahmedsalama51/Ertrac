# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

{
    'name': "EgyMentors Project/Purchase Report[ERTRAC]",
    'author': 'EgyMentors, Ahmed Salama',
    'category': 'Project',
    'summary': """Project Ertrack Report""",
    'website': 'http://www.egymentors.com',
    'license': 'AGPL-3',
    'description': """
""",
    'version': '10.0',
    'depends': ['project', 'sale', 'hr_timesheet', 'sale_timesheet', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        
        'data/task_headers_data.xml',
        'data/task_type_data.xml',
        
        'reports/reports.xml',
        
        'views/task_ertrack_report_view.xml',
        'views/project_task_view_changes.xml',
        'views/task_header_view.xml',
        'views/task_type_view.xml',
        'views/sale_order_view_changes.xml',
        'views/product_view_changes.xml',
        
        'wizard/work_progress_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
