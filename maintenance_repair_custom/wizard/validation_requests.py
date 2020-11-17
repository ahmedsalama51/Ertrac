# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError



class ValidateRequests(models.TransientModel):
    _name = 'validation.requests'


    def validation_action(self):
        requests = self.env['maintenance.request'].browse(self._context['active_ids'])
        stage_draft = self.env['maintenance.stage'].search([('name','=','Draft')])
        stage_new_request = self.env['maintenance.stage'].search([('name','=','New Request')])
        if requests.stage_id.id == stage_draft.id:
            requests.stage_id = stage_new_request.id
        else:
            raise UserError("Validation only occurs on (Draft) stage Requests")
        return {'type':'ir.actions.act_window_close'}
