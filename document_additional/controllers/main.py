# -*- coding: utf-8 -*-
import base64
import io
import mimetypes
import os

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class MyDocuments(http.Controller):

    @http.route('/my/documents', type='http', auth="user", website=True)
    def my_document_details(self, **kwargs):
        user_details = request.env['res.users'].sudo().search([('id', '=', request.env.uid)])
        documents = request.env['document.document'].sudo().search(
            [('user_ids', 'in', user_details.ids), ('active', '=', True)])
        return request.render("document_additional.portal_document_details", {'documents': documents})

    @http.route(['/attachment/download'], type='http', auth='user')
    def download_attachment(self, attachment_id):
        attachment = request.env['document.document'].sudo().search([('id', '=', int(attachment_id))])
        if attachment:
            data = io.BytesIO(base64.standard_b64decode(attachment.document))
            filename = attachment.name
            return http.send_file(data, filename=filename, as_attachment=True)
        else:
            return request.not_found()


class DocumentCount(CustomerPortal):

    @http.route()
    def home(self, **kw):
        response = super(DocumentCount, self).home(**kw)
        user_details = request.env['res.users'].sudo().search([('id', '=', request.env.uid)])
        document_count = request.env['document.document'].sudo().search_count([('user_ids', 'in', user_details.ids)])
        response.qcontext.update({
            'document_count': document_count
        })
        return response
