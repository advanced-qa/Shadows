# -*- coding: utf-8 -*-

{
    'name': "Invoice Multi level Approval",
    'version': '14.0.1.0.0',
    'summary': """This module add the multiple approval option for invoice,
    			  bill,refund and credit notes.""",
    'description': """This module add the multiple approval option for invoice,
    bill,refund and credit notes.""",
    'category': 'Accounting',
    'author': 'Cybrosys Techno Solutions & Advanced Solutions',
    'website': "https://www.advanced.qa",
    'depends': ['account'],
    'data': [
        'data/data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/invoice_approval_view.xml',
        'views/account_move_inherited.xml',
    ],
    'license': "AGPL-3",
    'images': [],
    'installable': True,
    'application': True,
}
