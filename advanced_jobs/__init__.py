# -*- coding: utf-8 -*-
from . import models
from . import controllers
from odoo import api, SUPERUSER_ID


def _fields_whitelist(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_dob'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_gender'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_nationality'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_residence'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_whatsapp'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_skype'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['partner_linkedin'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['education'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['certification'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['experience'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['current_position'])
    env['ir.model.fields'].formbuilder_whitelist('hr.applicant', ['current_employer'])

