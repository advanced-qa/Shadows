# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Linto C.T, Milind (odoo@cybrosys.com)
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
    'name': 'Dynamic Financial Reports',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'summary': """Dynamic Balance Sheet & Profit & Loss Report with drill 
                down – Community Edition""",
    'description': "This module creates dynamic Balance Sheet and P & L "
                   "Dynamic financial report, financial report"
                   "reports"
                   "Balance Sheet & Profit and Loss Reports, Financial report,"
                   " Dynamic Report, Odoo 14 Accounting",
    'author': 'Cybrosys Techno Solutions & Advanced Solutions',
    'website': "https://www.advanced.qa",
    'company': 'Advanced Solutions',
    'depends': ['base', 'base_accounting_kit'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'wizard/financial_report_view.xml',
        'report/report.xml',
        'report/report_template_pdf.xml'
            ],
    'qweb': [
        'static/src/xml/report_tmpl.xml'],
    'license': 'OPL-1',
    'price': 19,
    'currency': 'EUR',
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}    
