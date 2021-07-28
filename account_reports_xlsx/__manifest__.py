# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Technologies (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

{
    'name': 'Accounting Report Excel',
    'version': '14.0.1.0.0',
    'author': 'Cybrosys Techno Solutions & Advanced Solutions ',
    'website': "https://www.advanced.qa",
    'category': 'Accounting',
    'summary': """Generates Excel report for Partner Ledger,General Ledger,Balance Sheet,
                Profit and Loss,Aged Partner Balance.""",
    'description': """Generates Excel reports, 
                    Accounting Reports, Odoo 14, Odoo 14 report,Odoo 14 Accounting Report,Odoo 14 Excel Report, Partner Profit and Loss,Aged Partner Balance,Ledger,General Ledger,Balance Sheet,Account Reports, Excel Report, Excel, Xlsx Report, xlsx,Accounting Excel Reports, Account Excel Reports""",
    'depends': ['base', 'account'],
    'data': [
        'views/action_manager.xml',
        'security/ir.model.access.csv',
        'views/report_agedpartnerbalance.xml',
        'wizard/partner_ledger_wizard_view.xml',
        'views/partner_ledgerreport.xml',
        'wizard/account_report_aged_partner_balance_view.xml',
        'wizard/account_report_general_ledger_view.xml',
        'wizard/account_financial_report_view.xml',
        'views/account_financial_report_data.xml',
    ],
    'license': 'OPL-1',
    'price': 19.99,
    'currency': 'EUR',
    'images': [],
    'auto_install': False,
    'installable': True,
    'application': True,
}
