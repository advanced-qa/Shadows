# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
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

import io
import json

from odoo import models, fields
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class AccountFinancialReport(models.TransientModel):
    _inherit = "financial.report"

    view_format = fields.Selection([
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal')],
        default='vertical',
        string="Format")

    def view_report(self):
        """This function will be executed when we click the view button from the wizard.
        Based on the values provided in the wizard, this function will evoke the
        corresponding client action in js"""
        self.ensure_one()
        data = dict()
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(
            ['date_from', 'enable_filter', 'debit_credit', 'date_to',
             'account_report_id', 'target_move', 'view_format',
             'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(
            used_context,
            lang=self.env.context.get('lang') or 'en_US')

        report_lines = self.get_account_lines(data['form'])
        # find the journal items of these accounts
        journal_items = self.find_journal_items(report_lines, data['form'])
        report_name = ''
        report_id = parent = id = None

        def set_report_level(rec):
            """This function is used to set the level of each item.
            This level will be used to set the alignment in the dynamic reports."""
            level = 1
            if not rec['parent']:
                return level
            else:
                for line in report_lines:
                    key = 'a_id' if line['type'] == 'account' else 'id'
                    if line[key] == rec['parent']:
                        return level + set_report_level(line)

        # finding the root
        for item in report_lines:
            print("item", item)
            item['balance'] = round(item['balance'], 2)
            if not item['parent']:
                item['level'] = 1
                parent = item
                report_name = item['name']
                id = item['id']
                report_id = item['r_id']
            else:
                item['level'] = set_report_level(item)
        currency = self._get_currency()
        # checking view type

        print("parent", parent)
        if data['form'].get('view_format') == 'horizontal':
            return {
                'name': "Financial Reports",
                'type': 'ir.actions.client',
                'tag': 'reports_view_horizontal',
                'params': {
                    'parent': parent,
                    'report_lines': report_lines,
                    'journal_items': journal_items,
                    'form': data['form'],
                    'currency': currency
                }
            }
        else:
            return {
                'name': "Financial Reports",
                'type': 'ir.actions.client',
                'tag': 'report_bs_view',
                'id': id,
                'params': {
                    'parent': parent,
                    'report_id': report_id,
                    'report_name': report_name,
                    'report_lines': report_lines,
                    'journal_items': journal_items,
                    'form': data['form'],
                    'currency': currency
                }

            }

    def print_pdf(self, view_data):
        """ This function will generate pdf of the dynamic view """
        self.ensure_one()
        data = dict()
        data['form'] = self.read(
            ['date_from', 'enable_filter', 'debit_credit', 'date_to',
             'target_move', 'view_format'])[0]
        data = {
            'data': data['form'],
            'html_data': view_data
        }
        return self.env.ref(
            'accounting_dynamic_reports.financial_report_export_pdf').report_action(
            self, data)

    def view_report_xlsx(self):
        """ This function will generate excel report """
        self.ensure_one()
        data = dict()
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(
            ['date_from', 'enable_filter', 'debit_credit', 'date_to',
             'account_report_id', 'target_move', 'view_format',
             'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(
            used_context,
            lang=self.env.context.get('lang') or 'en_US')

        report_lines = self.get_account_lines(data['form'])
        # find the journal items of these accounts
        journal_items = self.find_journal_items(report_lines, data['form'])

        report_name = ''
        report_id = id = parent = None

        def set_report_level(rec):
            """This function is used to set the level of each item.
            This level will be used to set the alignment in the dynamic reports."""
            level = 1
            if not rec['parent']:
                return level
            else:
                for line in report_lines:
                    key = 'a_id' if line['type'] == 'account' else 'id'
                    if line[key] == rec['parent']:
                        return level + set_report_level(line)

        # finding the root
        for item in report_lines:
            item['balance'] = round(item['balance'], 2)
            if not item['parent']:
                item['level'] = 1
                parent = item
                report_name = item['name']
                id = item['id']
                report_id = item['r_id']
            else:
                item['level'] = set_report_level(item)
        report_name = parent['name']
        data['report_lines'] = report_lines,
        data['journal_items'] = journal_items,
        data['currency'] = self._get_currency()
        return {
            'type': 'ir_actions_xlsx_download',
            'data': {'model': 'financial.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': report_name,
                     }
        }

    def get_xlsx_report(self, data, response):
        """ Generate excel report  """
        output = io.BytesIO()
        report_lines = data['report_lines'][0]
        currency = data['currency']
        data = data['form']
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        format1 = workbook.add_format(
            {'font_size': 16, 'align': 'center', 'bg_color': '#D3D3D3',
             'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center'})
        format12 = workbook.add_format({'font_size': 10})
        format1.set_font_color('#000080')
        format1.set_align('center')
        format2 = workbook.add_format(
            {'font_size': 12, 'bold': True, 'bg_color': '#D3D3D3'})
        format2.set_align('center')
        format3 = workbook.add_format({'font_size': 10, 'bold': True})
        format4 = workbook.add_format(
            {'font_size': 10, 'bold': True, 'border': 1,
             'bg_color': '#D2D1D1'})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        format6 = workbook.add_format({'font_size': 10, 'bold': True})
        format8 = workbook.add_format({'font_size': 10})
        format7 = workbook.add_format({'font_size': 10, 'border': 1})
        format9 = workbook.add_format({'font_size': 10, 'border': 1})
        format10 = workbook.add_format(
            {'font_size': 10, 'border': 1, 'bold': True})
        format1.set_align('center')
        format4.set_align('center')
        format3.set_align('right')
        format5.set_align('center')
        format6.set_align('right')
        format9.set_align('left')
        format10.set_align('left')
        format8.set_align('right')
        format7.set_align('right')
        format12.set_align('center')
        if data['date_from']:
            sheet.write('A2', 'Date From', format6)
            sheet.write('B2', str(data['date_from']), format7)
        if data['date_to']:
            sheet.write('C2', 'Date To', format6)
            sheet.write('D2', str(data['date_to']), format7)
        sheet.merge_range('A5:D6', self.env['account.financial.report'].browse(
            data['account_report_id'][0]).name, format1)
        if data['debit_credit']:
            sheet.set_column(0, 7, 18)
            sheet.write('A8', 'Name', format4)
            sheet.write('B8', 'Debit', format4)
            sheet.write('C8', 'Credit', format4)
            sheet.write('D8', 'Balance', format4)
            row = 9
            col = 0
            for lines in report_lines:
                sheet.write(row, col + 0, lines['name'], format10)
                sheet.write(row, col + 1, str(lines['debit']) + currency,
                            format7)
                sheet.write(row, col + 2, str(lines['credit']) + currency,
                            format7)
                sheet.write(row, col + 3, str(lines['balance']) + currency,
                            format7)
                row += 1
        else:
            sheet.merge_range('A8:B8', 'Name', format4)
            sheet.merge_range('C8:D8', 'Balance', format4)
            row = 8
            col = 0
            for lines in report_lines:
                sheet.merge_range(row, col + 0, row, col + 1, lines['name'],
                                  format10)
                sheet.merge_range(row, col + 2, row, col + 3,
                                  str(lines['balance']) + currency, format7)
                row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
