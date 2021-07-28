from odoo import api, fields, models, _


class JobsForm(models.Model):
    """ Additional fields for applicant form"""
    _inherit = 'hr.applicant'

    partner_dob = fields.Date("Date of birth")
    partner_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], "Gender")
    partner_nationality = fields.Many2one('res.country', "Nationality")
    partner_residence = fields.Many2one('res.country', "Country of residence")
    partner_whatsapp = fields.Char("Whatsapp")
    partner_skype = fields.Char("Skype")
    partner_linkedin = fields.Char("Linkedin")
    education = fields.Char("Education")
    certification = fields.Char("Certification")
    experience = fields.Char("Experience")
    current_position = fields.Char("Current position")
    current_employer = fields.Char("Current employer")