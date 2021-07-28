# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Technologies(odoo@cybrosys.com)
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
    'name': "Customer Followup",
    'version': '14.0.1.0.0',
    'summary': """Implements Customer Followups""",
    'description': """Implements Customer accounting followups for late payments """,
    'author': "Cybrosys Techno Solutions & Advanced Solutions ",
    'maintainer': 'Advanced Solutions',
    'company': "Advanced Solutions",
    'website': "https://www.Advanced.qa",
    'category': 'Accounting',
    'depends': ['account', 'mail', 'base_accounting_kit'],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'views/followup_setting.xml',
        'report/report.xml',
        'report/template.xml',
        'report/cron_report.xml',
        'data/followup_mail_template.xml',
        'data/after_due_date.xml',
        'data/before_due_date.xml',
        'views/res_partner_inherit.xml',
        'report/print.xml'
        ],
    'license': 'OPL-1',
    'price': 29,
    'currency': 'EUR',   
    'installable': True,          
}
