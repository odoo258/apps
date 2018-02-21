# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http
from odoo.addons.survey.controllers.main import WebsiteSurvey
import re
import json


class WebSurvey(WebsiteSurvey):

    # Survey start
    @http.route()
    def start_survey(self, survey, token=None, **post):
        response = super(WebSurvey, self).start_survey(
            survey, token)
        response.qcontext.update({'lead_id': post.get('lead_id')})
        return response

    # Survey display
    @http.route()
    def fill_survey(self, survey, token, prev=None, **post):
        values = []
        if post.get('lead_id'):
            current_lead = int(post.get('lead_id'))
            lead = request.env['crm.lead'].browse(current_lead)
            response = super(WebSurvey, self).fill_survey(
                survey, token, prev)
            questions = survey.page_ids.question_ids
            for records in questions:
                related_lead_name = records.related_lead.name
                if related_lead_name:
                    if records.related_lead.ttype == 'many2one':
                        value1 = getattr(lead, related_lead_name).name
                        values.append({
                            'field': records,
                            'value': value1
                        })
                    elif records.related_lead.ttype == 'boolean':
                        value2 = getattr(lead, str(related_lead_name))
                        values.append({
                            'field': records,
                            'value': value2
                        })
                    elif records.related_lead.ttype == 'one2many':
                        raise ValidationError(
                            _('Values of one2many fields are not returned.'))
                    else:
                        if related_lead_name == 'phone':
                            value3 = getattr(lead, related_lead_name)
                            value3 = re.sub('[+\s+]', '', value3)
                            values.append({
                                'field': records,
                                'value': value3
                            })
                        else:
                            value3 = getattr(lead, related_lead_name)
                            values.append({
                                'field': records,
                                'value': value3
                            })
            response.qcontext.update({
                'test': values,
                'lead_id': current_lead,
            })
            res = response.qcontext
            return response

    @http.route()
    def submit(self, survey, **post):
        lead = int(post.get('lead_id'))
        crm = request.env['crm.lead'].browse(lead)
        for k, v in post.items():
            value = k.split('_')
            if len(value) == 3 and value[0].isdigit():
                value = int(value[2])
                question = request.env['survey.question'].browse(value)
                name = question.related_lead.name
                k = name.split('_')
                if len(k) > 1:
                    if k[1] == 'id':
                        vals = setattr(crm, name, 1)
                    else:
                        vals = setattr(crm, name, v)
                else:
                    vals = setattr(crm, name, v)
        page_id = int(post['page_id'])
        questions = request.env['survey.question'].search(
            [('page_id', '=', page_id)])
        errors = {}
        for question in questions:
            answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
            errors.update(question.validate_question(post, answer_tag))
        ret = {}
        if len(errors):
            ret['errors'] = errors
        else:
            try:
                user_input = request.env['survey.user_input'].sudo().search(
                    [('token', '=', post['token'])], limit=1)
            except KeyError:
                return request.render("website.403")
            user_id = request.env.user.id if user_input.type != 'link' else SUPERUSER_ID
            for question in questions:
                answer_tag = "%s_%s_%s" % (survey.id, page_id, question.id)
                request.env['survey.user_input_line'].sudo(user=user_id).save_lines(
                    user_input.id, question, post, answer_tag)
            go_back = post['button_submit'] == 'previous'
            next_page, _, last = request.env['survey.survey'].next_page(
                user_input, page_id, go_back=go_back)
            vals = {'last_displayed_page_id': page_id}
            if next_page is None and not go_back:
                vals.update({'state': 'done'})
            else:
                vals.update({'state': 'skip'})
            user_input.sudo(user=user_id).write(vals)
            ret['redirect'] = '/survey/fill/%s/%s/?lead_id=%s' % (
                survey.id, post['token'], post['lead_id'])
            if go_back:
                ret['redirect'] += '/prev'
        return json.dumps(ret)
