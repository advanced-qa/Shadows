from datetime import timedelta, datetime, date
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectContract(models.Model):
    _name = 'project.contract'

    name = fields.Char(string="Name", translate=True, required=True)
    contract_period = fields.Selection([('daily', 'Daily'), ('monthly', 'Monthly'), ('yearly', 'Yearly')],
                                       string="Contract Period", required=True)
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    first_party = fields.Many2one('res.partner', string="First Party")
    second_party = fields.Many2one('res.partner', string="Second Party")
    description = fields.Text(string="Description")
    terms = fields.Text(string="Terms and Conditions")
    contract_pdf = fields.Binary(string="Attachment")


class ProjectTemplates(models.Model):
    _name = 'project.template'

    name = fields.Char("Template Name", required=True)
    bom_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines')
    bom_qtys = fields.One2many('project.bom', 'bom_project', string="Materials")
    summary = fields.Text(string="Details", readonly=True)

    def get_summary(self):
        if self.bom_qtys:
            materials = len(self.bom_qtys)
            to_purchase = 0
            on_hand = 0
            is_service = 0
            service_details = ''
            for items in self.bom_qtys:
                if items.to_purchase:
                    to_purchase += 1
                if items.to_sales:
                    on_hand += 1
                if items.is_service:
                    is_service += 1
                if items.products.type == 'service':
                    service = "\n* For " + str(items.products.name) + " " + \
                              str(items.exp_hours) + " Hours Is Expected"
                    service_details += service

            text = "Last Updated : " + str(fields.Datetime.now()) + \
                   "\n" + "Total Materials : " + str(materials) + \
                   "\n" + "No. Of Materials To Purchase : " + str(to_purchase) + \
                   "\n" + "Materials In Stock : " + str(on_hand) + \
                   "\n" + "No.of Services Included : " + str(is_service)
            self.summary = text + service_details


class ProjectPlanning(models.Model):
    _name = 'project.bom'

    @api.onchange('products')
    def _set_product_price(self):
        self.product_price = self.products.lst_price
        if self.products.type == 'service':
            self.is_service = True
        if self.products.type != 'service':
            self.is_service = False

    @api.model
    def create(self, vals_list):
        if vals_list.get('to_purchase') == vals_list.get('to_sales') == vals_list.get('is_service') == False:
            product = self.env['product.template'].browse(int(vals_list.get('products'))).name
            raise UserError('Please select any material status for the product %s' % product)
        return super(ProjectPlanning, self).create(vals_list)

    def write(self, vals):
        res = super(ProjectPlanning, self).write(vals)
        rec = self.browse(int(self._origin.id))
        if rec.is_service == rec.to_sales == rec.to_purchase == False:
            product = self.env['product.template'].browse(int(rec.products)).name
            raise UserError('Please select any material status for the product %s' % product)
        return res

    @api.onchange('is_service')
    def _set_service_product(self):
        self.products.type = 'service'

    bom_project = fields.Many2one('project.template')
    products = fields.Many2one('product.template', string="Product", required=True)
    product_price = fields.Float(string="Price")
    product_qty = fields.Float(string="Quantity", required=True, default=1.0)
    to_purchase = fields.Boolean(string="To Purchase")
    to_sales = fields.Boolean(string="In Stock")
    is_service = fields.Boolean(string="Service")
    exp_hours = fields.Float(string="Expected Hours")
    no_persons = fields.Integer(string="Factor", default=1,
                                help="Eg: no of persons, Here expected hours will be multiplied by this factor ")
    total_amount = fields.Float(string="Total Amount")

    def calculate_hours(self):
        self.total_amount = self.product_price * self.exp_hours * self.no_persons


class SalesOrderContract(models.Model):
    _inherit = 'sale.order'

    contract_selection = fields.Many2one('project.contract', string="Contract")
    project_name = fields.Char(string="Project Name")
    project_temp = fields.Many2one('project.template', string="Project Template")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('planning', 'Planning'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_planning(self):
        self.write({'state': 'planning'})

    def action_view_contract(self):
        return {
            'name': _('Contracts'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.contract',
            'domain': [('second_party', '=', self.partner_id.id)],
            'context': {'default_second_party': self.partner_id.id}
        }

    @api.onchange('project_temp')
    def add_project_templates(self):
        if self.project_temp:
            for items in self.project_temp.bom_qtys:
                if items.to_sales:
                    self.order_line = [
                        (0, 0, {'product_id': items.products.id, 'price_unit': items.product_price,
                                'product_uom_qty': items.product_qty})]
