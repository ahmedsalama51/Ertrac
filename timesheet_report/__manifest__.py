# -*- coding: utf-8 -*-
{
    'name': "Report Timesheet Ertrac",

    'summary': """
        Create Report on Taks of project""",

    'description': """
        Creates a report xlsx depending on company needs.
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','hr_timesheet','report_xlsx'],
    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/view.xml',
        'reports/reports.xml',
        ],
}