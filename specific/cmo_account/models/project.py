# -*- coding: utf-8 -*-

from openerp import fields, models, api
from openerp.exceptions import ValidationError
# TODO: foreign key use, idex and ondelete


class ProjectProject(models.Model):
    _inherit = 'project.project'

    invoice_related_ids = fields.One2many(
        'account.invoice',
        'project_ref_id',
        string='Related Invoice',
        domain=[('type', '=', 'out_invoice'), ],

    )
    is_paid = fields.Boolean(
        string='is paid',
        compute='_compute_invoice_related_ids',
    )

    @api.multi
    @api.depends('is_paid', 'invoice_related_ids', 'invoice_related_ids.state')
    def _compute_invoice_related_ids(self):
        for project in self:
            project_state = project.state
            if project_state not in (
                    'draft', 'validate', 'open',
                    'pending', 'cancelled', 'close'):
                invoice_open = project.invoice_related_ids.filtered(
                    lambda r: r.state in ('open', 'paid')
                )
                invoice_paid = project.invoice_related_ids.filtered(
                    lambda r: r.state in ('paid')
                )
                if invoice_paid and \
                        (len(invoice_paid) == len(project.invoice_related_ids)):
                    project.write({'state': 'paid'})
                elif invoice_open:
                    project.write({'state': 'invoices'})
                else:
                    project.write({'state': 'ready_billing'})

    @api.multi
    def quotation_relate_project_tree_view(self):
        self.ensure_one()
        domain = [
            ('project_related_id', 'like', self.id),
            ('order_type', '=', 'quotation'),
        ]
        action = self.env.ref('sale.action_quotations')
        result = action.read()[0]
        result.update({'domain': domain})
        return result
