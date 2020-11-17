# -*- coding: utf-8 -*-
{
    'name': "Maintenance Repair Relation",

    'summary': """
        Create a relation between maintenance and repair modules.""",

    'description': """
        Whenever creating Equipment it creates corresponding product,
        Whenever creating Maintnance order it create repair order in corresponding,
        You can create multiple maintenance requests from a tree view and validate them too
        without seeing all the details of each request.
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['maintenance','repair'],

    # always loaded
    'data': [
        'data/date.xml',
        #'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/validation_requests.xml',
    ],
}
