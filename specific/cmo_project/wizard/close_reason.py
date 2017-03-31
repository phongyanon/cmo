# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProjectCloseReason(models.TransientModel):
    _name = 'project.close.reason'

    close_reason = fields.Selection([
        ('close', "Closed"),
        ('reject', "Reject"),
        ('lost', "Lost"),
    ])

    @api.one
    def confirm_close(self, context=None):
        reason = self.browse(self.id)
        Project = self.env['project.project']
        project = Project.browse(context.get('active_id'))

        project.write({'state': 'close',
                       'close_reason': reason.close_reason,
                       })
        return {}
