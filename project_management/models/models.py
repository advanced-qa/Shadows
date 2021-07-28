# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ProjectManagement(models.Model):
    _inherit = 'project.project'

    budget = fields.Float('Project Budget')
    project_lock = fields.Selection([('lock', 'Lock Project'), ('unlock', 'Unlock Project')], string="Project status",
                                    required=True)
    current_purchased = fields.Monetary("Total Purchased", compute='_calculate_total_purchased')
    current_expensed = fields.Monetary("Total Expensed", compute='_calculate_total_expensed')
    project_warehouse = fields.Many2one('stock.location', "Warehouse Location")
    project_phases = fields.Many2many('project.task.phase')
    project_purchases = fields.Many2many('purchase.order')
    project_expenses = fields.Many2many('hr.expense')
    project_assets = fields.Many2many('account.asset.asset')
    project_set = fields.Boolean()
    project_todo = fields.Many2many('project.todo', 'project_id')
    project_plan = fields.Text()
    project_planning = fields.One2many('project.planning', 'project_id')
    compute_field = fields.Boolean(string="check field", compute='get_user')

    @api.model
    def create(self, vals_list):
        res = super(ProjectManagement, self).create(vals_list)
        res.project_set = True
        return res

    @api.depends('compute_field')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('project.group_project_user') and not res_user.has_group(
                'project.group_project_manager'):
            self.compute_field = True
        else:
            self.compute_field = False

    @api.depends('project_purchases.amount_total')
    def _calculate_total_purchased(self):

        for order in self:
            total_purchased = 0.0
            items_dict = []
            for data in order.project_purchases:
                for data_items in data._origin.order_line:
                    items_dict.append({'item': data_items.product_id.id, 'quantity': data_items.product_qty,
                                       'price': data_items.price_unit})

            for line in order.project_purchases:
                for items in line._origin.order_line:
                    obj = self.env['project.planning'].search(
                        [('project_id', '=', order._origin.id), ('product_id', '=', items.product_id.id)])
                    product_count = 0
                    for index in items_dict:
                        if index['item'] == items.product_id.id:
                            product_count += index['quantity']
                    if not obj:
                        raise ValidationError(
                            _('You have to get the permission for purchase this product. (Product: %s)',
                              items.name))
                    if obj:
                        if product_count > float(obj.product_count):
                            raise ValidationError(
                                _('Planned quantities for the product %s is %s' % (items.name, obj.product_count)))
                        if items.price_unit > float(obj.product_price):
                            raise ValidationError(
                                _('Planned price for the product %s is %s' % (items.name, obj.product_price)))
                total_purchased += line.amount_total

            order.update({
                'current_purchased': total_purchased,
            })
            self.check_project_budget()

    @api.depends('project_expenses.total_amount')
    def _calculate_total_expensed(self):
        for order in self:
            total_expense = 0.0
            for line in order.project_expenses:
                total_expense += line.total_amount
            order.update({
                'current_expensed': total_expense,
            })
            self.check_project_budget()

    def check_project_budget(self):
        for order in self:
            total = int(order.current_purchased) + int(order.current_expensed)
            if order.project_lock == 'lock':
                if total > order.budget:
                    raise ValidationError("Project Budget Limit Exceeded.")


class PurchaseProject(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one('project.project')
    project_temp = fields.Many2one('project.template', string="Project Template")

    @api.onchange('project_temp')
    def add_project_templates(self):
        if self.project_temp:
            for items in self.project_temp.bom_qtys:
                if items.to_purchase:
                    self.order_line = [
                        (0, 0, {'product_id': items.products.id, 'price_unit': items.product_price,
                                'product_qty': items.product_qty})]

    @api.onchange('order_line')
    def check_orderline(self):
        project_id = self.env['project.project'].browse(int(self.project_id))
        if project_id:
            for items in self.order_line:
                obj = self.env['project.planning'].search(
                    [('project_id', '=', project_id.id), ('product_id', '=', items.product_id.id)])
                if not obj:
                    raise UserError(
                        _('You have to get the permission for purchase this product. (Product: %s)',
                          items.product_id.name))
                if obj:
                    if items.product_qty > float(obj.product_count):
                        raise UserError(
                            _('Planned quantities for the product %s is %s' % (
                                items.product_id.name, obj.product_count)))
                    if items.product_qty <= float(obj.product_count):
                        items_selected = []
                        products_count = 0
                        previous_order = self.search([('project_id', '=', project_id.id)])
                        for lines in previous_order:
                            for line in lines.order_line:
                                items_selected.append({'item': line.product_id.id, 'quantity': line.product_qty,
                                                       'price': line.price_unit})

                        for counts in items_selected:
                            if counts['item'] == items.product_id.id:
                                products_count += counts['quantity']

                        if float(products_count) + float(items.product_qty) > float(obj.product_count):
                            difference = float(obj.product_count) - float(products_count)
                            raise UserError(
                                _(
                                    'Planned quantities for the product %s is %s. Quantities are already purchased is %s' % (
                                        items.name, obj.product_count, products_count)))

                    if items.price_unit > float(obj.product_price):
                        raise UserError(
                            _('Planned price for the product %s is %s' % (items.name, obj.product_price)))


class ExpenseProject(models.Model):
    _inherit = 'hr.expense'

    project_id = fields.Many2one('project.project')


class AssetsProject(models.Model):
    _inherit = 'account.asset.asset'

    project_id = fields.Many2one('project.project')


class ProjectPlanning(models.Model):
    _name = "project.planning"

    project_id = fields.Many2one('project.project')
    product_id = fields.Many2one('product.product', string="Items")
    product_count = fields.Float("Count")
    product_price = fields.Float("Price")


class ProjectTodo(models.Model):
    _name = 'project.todo'

    name = fields.Char(string="item", required=True)
    project_id = fields.Many2one('project.project')


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    task_name = fields.Char()

    def _timesheet_create_task(self, project):
        """ Generate task for the given so line, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        print("Hello")
        values = self._timesheet_create_task_prepare_values(project)
        stage = self.env['project.task.type'].sudo().search([('name', '=', self.task_name)])
        if stage:
            values.update({'stage_id': stage.id})
        if not stage:
            stage = self.env['project.task.type'].sudo().create({'name': self.task_name, 'project_ids': project})
        values.update({'stage_id': stage.id})
        task = self.env['project.task'].sudo().create(values)
        self.write({'task_id': task.id})
        # post message on task
        task_msg = _(
            "This task has been created from: <a href=# data-oe-model=sale.order data-oe-id=%d>%s</a> (%s)") % (
                       self.order_id.id, self.order_id.name, self.product_id.name)
        task.message_post(body=task_msg)
        return task

    def _timesheet_service_generation(self):
        """ For service lines, create the task or the project. If already exists, it simply links
            the existing one to the line.
            Note: If the SO was confirmed, cancelled, set to draft then confirmed, avoid creating a
            new project/task. This explains the searches on 'sale_line_id' on project/task. This also
            implied if so line of generated task has been modified, we may regenerate it.
        """
        so_line_task_global_project = self.filtered(
            lambda sol: sol.is_service and sol.product_id.service_tracking == 'task_global_project')
        so_line_new_project = self.filtered(
            lambda sol: sol.is_service and sol.product_id.service_tracking in ['project_only', 'task_in_project'])

        # search so lines from SO of current so lines having their project generated,
        # in order to check if the current one can
        # create its own project, or reuse the one of its order.
        map_so_project = {}
        if so_line_new_project:
            order_ids = self.mapped('order_id').ids
            so_lines_with_project = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), (
                'product_id.service_tracking', 'in', ['project_only', 'task_in_project']),
                                                 ('product_id.project_template_id', '=', False)])
            map_so_project = {sol.order_id.id: sol.project_id for sol in so_lines_with_project}
            so_lines_with_project_templates = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), (
                'product_id.service_tracking', 'in', ['project_only', 'task_in_project']),
                                                           ('product_id.project_template_id', '!=', False)])
            map_so_project_templates = {(sol.order_id.id, sol.product_id.project_template_id.id): sol.project_id for sol
                                        in so_lines_with_project_templates}
        # search the global project of current SO lines, in which create their task

        map_sol_project = {}
        if so_line_task_global_project:
            map_sol_project = {sol.id: sol.product_id.with_company(sol.company_id).project_id for sol in
                               so_line_task_global_project}

        def _can_create_project(sol):
            if not sol.project_id:
                if sol.product_id.project_template_id:
                    return (sol.order_id.id, sol.product_id.project_template_id.id) not in map_so_project_templates
                elif sol.order_id.id not in map_so_project:
                    return True
            return False

        def _determine_project(so_line):
            """Determine the project for this sale order line.
            Rules are different based on the service_tracking:

            - 'project_only': the project_id can only come from the sale order line itself
            - 'task_in_project': the project_id comes from the sale order line only if no project_id was configured
              on the parent sale order"""
            if so_line.product_id.service_tracking == 'project_only':
                return so_line.project_id
            elif so_line.product_id.service_tracking == 'task_in_project':
                return so_line.order_id.project_id or so_line.project_id
            return False

        # task_global_project: create task in global project
        for so_line in so_line_task_global_project:
            if not so_line.task_id:
                if map_sol_project.get(so_line.id):
                    so_line._timesheet_create_task(project=map_sol_project[so_line.id])

            # project_only, task_in_project: create a new project, based or not on a template (1 per SO). May be create a task too.
            # if 'task_in_project' and project_id configured on SO, use that one instead
            line_selection = ''
            for so_line in self:
                if so_line.display_type == 'line_section':
                    title = so_line.display_name
                    if so_line.order_id.project_name:
                        title = so_line.display_name.replace(so_line.order_id.name, so_line.order_id.project_name)
                    line_selection = title
                    pass
                if so_line.display_type != 'line_section':
                    so_line.write({'task_name': line_selection})
                    project = _determine_project(so_line)
                    if not project and _can_create_project(so_line):
                        project = so_line._timesheet_create_project()
                        if so_line.product_id.project_template_id:
                            map_so_project_templates[
                                (so_line.order_id.id, so_line.product_id.project_template_id.id)] = project
                        else:
                            map_so_project[so_line.order_id.id] = project
                    elif not project:
                        # Attach subsequent SO lines to the created project
                        so_line.project_id = (
                                map_so_project_templates.get(
                                    (so_line.order_id.id, so_line.product_id.project_template_id.id))
                                or map_so_project.get(so_line.order_id.id)
                        )
                    if so_line.product_id.service_tracking == 'task_in_project':
                        if not project:
                            if so_line.product_id.project_template_id:
                                project = map_so_project_templates[
                                    (so_line.order_id.id, so_line.product_id.project_template_id.id)]
                            else:
                                project = map_so_project[so_line.order_id.id]
                        if not so_line.task_id:
                            so_line._timesheet_create_task(project=project)
