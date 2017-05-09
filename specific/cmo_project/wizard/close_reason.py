# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProjectCloseReason(models.TransientModel):
    _name = 'project.close.reason'
    

    close_reason = fields.Selection(
        selection="_get_close_reason_list",
    )

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
        if self.close_reason == 'lost': # project.write doesn't work
            project.lost_reason = self.lost_reason
            project.lost_by = self.lost_by
            project.reject_reason = None
            project.set_cancel()
        elif self.close_reason == 'reject':
            project.reject_reason = self.reject_reason
            project.lost_reason = None
            project.lost_by = None
            project.set_cancel()
        elif self.close_reason == 'cancel':
            project.lost_reason = None
            project.lost_by = None
            project.reject_reason = None
            project.set_cancel()
        elif self.close_reason == 'terminate':
            project.lost_reason = None
            project.lost_by = None
            project.reject_reason = None
            project.set_cancel()
        elif self.close_reason == 'close':
            project.lost_reason = None
            project.lost_by = None
            project.reject_reason = None
            project.set_done()
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def _get_close_reason_list(self):
        Project = self.env['project.project']
        context = self.env.context
        project_id = context.get('active_ids', False)
        project = Project.browse(project_id[0])
        vals = []
        if (project.state == "draft") or (project.state == "validate") :
            vals = [
                ('reject', 'Reject'),
                ('lost', 'Lost'),
                ('cancel', 'Cancelled'),
            ]
        elif (project.state == "open") or (project.state == "ready_billing") or (project.state == "invoices"):
            vals = [
                ('cancel', 'Cancelled'),
                ('terminate', 'Terminated'),
            ]
        elif (project.state == "received"):
            vals = [
                ('close', 'Completed'),
            ]
        return vals
