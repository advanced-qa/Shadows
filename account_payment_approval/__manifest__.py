# -*- coding: utf-8 -*-


{
    'name': 'Payment Approvals',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'summary': """ This modules enables approval feature in the payment.""",
    'description': """This modules enables approval feature in the payment. """,
    'author': ' Cybrosys Techno Solutions & Advanced Soluations',
    'sequence':1,
    'website': "https://www.advanced.qa",
    'depends': ['account'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_payment_view.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

