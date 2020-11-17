# -*- coding: utf-8 -*-
{
    'name': "Invoice Report Xlsx",

    'summary': """
        Create invoice Report in Xlsx Sheet""",

    'description': """
        This module is designed for Ertrac Company
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management','account','account_accountant','project','hr_timesheet','sale_timesheet','report_xlsx','invoice_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
