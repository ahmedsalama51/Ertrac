# -*- coding: utf-8 -*-
{
    'name': "Picking Customization",
    'summary': """ Analytic Tag Track""",
    'description': """
        This Module Tracks the Analytic tag values starting from the sale order
        to the stock picking to the journal entries created and The Analytic Tag Report
    """,

    'author': "EgyMentors Team",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'sale', 'account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
