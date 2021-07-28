# -*- coding: utf-8 -*-
{
    'name': "project_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project_report_pdf', 'project_task_timer', 'purchase', 'bi_odoo_project_phases', 'base_accounting_kit',
                'hr_expense', 'analytic', 'sale_project', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/demo.xml',
        'views/views.xml',
        'views/project_contract.xml',
        'views/project_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'post_init_hook': '_initial_setup',

}
