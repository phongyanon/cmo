# -*- coding: utf-8 -*-

from openerp import fields, models, api
from openerp.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # is_paid = fields.Boolean(
    #     string='is paid',
    #     compute='_compute_invoice_related_ids',
    # )
    #
    # @api.multi
    # @api.depends('is_paid', 'invoice_related_ids', 'invoice_related_ids.state')
    # def _compute_invoice_related_ids(self):
    #     for project in self:
    #         project_state = project.state
    #
    #         if project_state not in (
    #                 'draft', 'validate', 'open',
    #                 'pending', 'cancelled', 'close'):
    #             print('>>>>>>>>> 2 ', project_state)
    #             invoice_open = project.invoice_related_ids.filtered(
    #                 lambda r: r.state in ('open', 'paid')
    #             )
    #             invoice_paid = project.invoice_related_ids.filtered(
    #                 lambda r: r.state in ('paid')
    #             )
    #             print('>>>>>>>>> 2 ', invoice_open, invoice_paid)
    #             if invoice_paid and \
    #                     (len(invoice_paid) == len(project.invoice_related_ids)):
    #                 project._write({'state': 'close'})
    #             elif invoice_open:
    #                 # x=1/0
    #                 project._write({'state': 'invoices'})
    #             else:
    #                 project._write({'state': 'ready_billing'})
