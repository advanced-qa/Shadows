import base64
import json
import logging
import time
import datetime
import io
import os
import mimetypes

import werkzeug
import ast

from odoo import http, _
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from werkzeug.exceptions import NotFound
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

_logger = logging.getLogger(__name__)


class Payments(WebsiteHrRecruitment):

    @http.route('''/jobs/apply/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''', type='http', auth="public", website=True)
    def jobs_apply(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()
        countries = request.env['res.country'].sudo().search([])
        error = {}
        default = {}
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')
        return request.render("website_hr_recruitment.apply", {
            'job': job,
            'countries': countries,
            'error': error,
            'default': default,
        })

    @http.route(['/job_apply'], type='http', csrf=False, auth='user', methods=['POST'], website=True)
    def apply_for_jobs(self, **kwargs):
        print(kwargs, "values")
        keys = ['partner_nationality', 'partner_residence', 'job_id', 'department_id']
        for key in keys:
            kwargs[key] = int(kwargs[key])
        obj = request.env['hr.applicant'].sudo().create(kwargs)
