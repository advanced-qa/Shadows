# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo import api, SUPERUSER_ID


def _initial_setup(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.config.settings'].group_analytic_accounting = True
    # env['ir.config_parameter'].sudo().set_param("group_analytic_tags", True)
