# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProjectCloseReason(models.TransientModel):
    _name = 'project.close.reason'

    close_reason = fields.Selection([
        ('close', 'Closed'),
        ('reject', 'Reject'),
        ('lost', 'Lost'),
    ])

    @api.multi
    def confirm_close(self, context=None):
        self.ensure_one()
        Project = self.env['project.project']
        project = Project.browse(context.get('active_id'))
        project.close_reason = self.close_reason
        project.set_done()
        return {'type': 'ir.actions.act_window_close'}
