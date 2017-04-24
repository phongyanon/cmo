# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProjectCloseReason(models.TransientModel):
    _name = 'project.close.reason'

    close_reason = fields.Selection([
        ('close', 'Completed'),
        ('reject', 'Reject'),
        ('lost', 'Lost'),
    ])
    lost_by = fields.Many2one(
        'res.partner',
        domain=[('category_id', 'like', 'Competitor'), ],
    )
    lost_reason = fields.Many2one(
        'project.lost.reason',
        string='Lost Reason',
    )
    reject_reason = fields.Many2one(
        'project.reject.reason',
        string='Reject Reason',
    )

    @api.multi
    def confirm_close(self, context=None):
        self.ensure_one()
        Project = self.env['project.project']
        project = Project.browse(context.get('active_id'))
        project.close_reason = self.close_reason
        if self.close_reason == 'lost':
            project.lost_reason = self.lost_reason
            project.lost_by = self.lost_by
            project.reject_reason = None
        elif self.close_reason == 'reject':
            project.reject_reason = self.reject_reason
            project.lost_reason = None
            project.lost_by = None
        else:
            project.lost_reason = None
            project.lost_by = None
            project.reject_reason = None
        project.set_done()
        return {'type': 'ir.actions.act_window_close'}
