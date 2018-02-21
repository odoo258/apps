from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    survey_input_ids = fields.One2many(
        'survey.user_input', 'survey_input_id', string='Surveys', readonly=True, index=True)
    survey_id = fields.Many2one(
        'survey.survey', related='stage_id.survey', string="Survey")

    @api.multi
    def action_start_survey(self):
        """ Open the website page with the survey form """
        self.ensure_one()
        if not self.survey_id.id:
            raise ValidationError(_('No survey is linked to this stage.'))
        else:
            response = self.env['survey.user_input'].create(
                {'survey_input_id': self.id, 'survey_id': self.survey_id.id, 'partner_id': self.partner_id.id, 'type': 'manually'})
            return self.survey_id.with_context(survey_token=response.token,
                                               id=self).action_start_survey()


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    survey = fields.Many2one('survey.survey')


class SurveyQue(models.Model):
    _inherit = 'survey.question'

    related_lead = fields.Many2one('ir.model.fields', domain=[
                                   ('model', '=', 'crm.lead')])


class SurveyInput(models.Model):
    _inherit = 'survey.user_input'

    survey_input_id = fields.Many2one('crm.lead')


class Survey(models.Model):
    _inherit = 'survey.survey'

    @api.multi
    def action_start_survey(self):
        """ Open the website page with the survey form """
        self.ensure_one()
        token = self.env.context.get('survey_token')
        trail = "/%s" % token if token else ""
        trail += '?lead_id=%s' % (self.env.context.get('id').id)
        return {
            'type': 'ir.actions.act_url',
            'name': "Start Survey",
            'target': 'self',
            'url': self.with_context(relative_url=True).public_url + trail,
        }
