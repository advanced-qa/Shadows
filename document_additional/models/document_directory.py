from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
from odoo.exceptions import Warning


class DocumentDirectory(models.Model):
    _inherit = 'document.directory'

    color = fields.Integer()
    workspace = fields.Char("Workspace", translate=True)
    company_id = fields.Many2many('res.company', string="Company", default=lambda self: self.env.company)
    main_directory = fields.Char()
    set_master_dir = fields.Boolean(string="Set Master Folder")

    @api.onchange('parent_id')
    def set_directory_users(self):
        for rec in self:
            if rec.parent_id.user_ids:
                rec.user_ids = rec.parent_id.user_ids

    @api.onchange('set_master_dir')
    def set_master_directory(self):
        for rec in self:
            if rec.set_master_dir:
                rec.main_directory = rec.name
                if rec._origin:
                    rec.set_master_parent(rec._origin, rec.main_directory, True)
            if not rec.set_master_dir:
                rec.main_directory = False
                if rec._origin:
                    rec.set_master_parent(rec._origin, rec.main_directory, False)

    def set_master_parent(self, value, Name, state):
        parent = value.id
        obj = self.env['document.directory'].search([('parent_id', '=', parent)])
        for rec in obj:
            if state:
                rec.main_directory = Name
            else:
                rec.main_directory = False
            rec.set_master_parent(rec, rec.main_directory, state)
        return


class DocumentDocument(models.Model):
    _inherit = 'document.document'

    expiry_date = fields.Date(string='Expiry Date', copy=False)
    user_ids = fields.Many2many('res.users', 'documents_user_rel', 'user_id', 'doc_id', string="Users", required=True)
    notification_period = fields.Integer("Notification period",
                                         help="how many days before the expiration users want to get notified",
                                         default=30)
    description = fields.Text("Notes", translate=True)
    department_id = fields.Many2one('hr.department', string='Department')

    @api.onchange('directory_id')
    def set_document_users(self):
        for rec in self:
            if rec.directory_id.user_ids:
                rec.user_ids = rec.directory_id.user_ids

    def mail_reminder(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.expiry_date:
                exp_date = i.expiry_date - timedelta(days=i.notification_period)
                if date_now >= exp_date:
                    for user in i.user_ids:
                        mail_content = "  Hello  " + user.name + ",<br>Your Document " + i.name + "is going to expire on " + \
                                       str(i.expiry_date) + ". Please renew it before expiry date"
                        main_content = {
                            'subject': _('Document-%s Expired On %s') % (i.name, i.expiry_date),
                            'author_id': self.env.user.partner_id.id,
                            'body_html': mail_content,
                            'email_to': user.work_email,
                        }
                        self.env['mail.mail'].create(main_content).send()

    @api.constrains('expiry_date')
    def check_expr_date(self):
        for rec in self:
            if rec.expiry_date:
                exp_date = rec.expiry_date
                if exp_date < date.today():
                    raise Warning('Your Document Is Already Expired.')

    def action_document_details(self):
        self.ensure_one()
        form_view = self.env.ref('document_additional.view_document_details')
        return {
            'name': _('Document Details'),
            'type': 'ir.actions.act_window',
            'views': [(form_view.id, 'form'), ],
            'res_model': 'document.document',
            'res_id': self.id,
            'target': 'new',
        }
