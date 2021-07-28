# -*- coding: utf-8 -*-


{
    'name': 'Advanced Cash Flow Statements',
    'version': '14.0.1.0.0',
    'summary': """Generate four levels of cash flow statement reports in PDF and Excel""",
    'description': """Generate four levels of cash flow statement reports in PDF and Excel, pdf report, excel report, cashflow,""",
    'author': ' Cybrosys Techno Solutions & Advanced Soluations',
    'sequence':1,
    'website': "https://www.advanced.qa",
    'category': 'Accounting',
    'depends': ['base', 'account'],
    'data': ['security/ir.model.access.csv',
             'wizard/account_wizard.xml',
             'views/action_manager.xml',
             'report/print_report.xml',
             'report/pdf_template.xml',
             ],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
