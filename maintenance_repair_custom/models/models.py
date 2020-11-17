# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)
    employee_id_custom = fields.Many2one('hr.employee',string='Employee')
    repair_id = fields.Many2one('repair.order', string='Repair')
    used_location = fields.Char('Location')
    quantity_equipment = fields.Integer('Quantity')

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            equipment_emp = self.env['maintenance.equipment'].search([('id','=',self.equipment_id.id)]).mapped('employee_id')
            equipment_emp2 = self.env['maintenance.equipment'].search([('id','=',self.equipment_id.id)]).mapped('location')
            self.employee_id_custom = equipment_emp[0]
            self.used_location = equipment_emp2[0]

        else:
            self.employee_id_custom = False
            self.used_location = False



    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        request = super(MaintenanceRequest, self).create(vals)
        if request.owner_user_id or request.user_id:
            request._add_followers()
        if request.equipment_id and not request.maintenance_team_id:
            request.maintenance_team_id = request.equipment_id.maintenance_team_id
        request.stage_id.name = 'Draft'
        request.activity_update()
        return request

