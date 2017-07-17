# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    quote_ref_id = fields.Many2one(
        'sale.order',
        string='Quotation Ref.',
        compute='_compute_quote_ref_id',
        readonly=True,
    )
    purchase_ref_id = fields.Many2one(
        'purchase.order',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    project_ref_id = fields.Many2one(
        'project.project',
        string='Project Ref.',
        compute='_compute_quote_ref_id',
    )
    quote_ref_number = fields.Char(
        string='Quotation Number',
        readonly=True,
        related='quote_ref_id.name',
    )
    quote_ref_date = fields.Datetime(
        string='Quotation Date',
        readonly=True,
        related='quote_ref_id.date_order',
    )
    quote_ref_event_date = fields.Char(
        string='Event Date',
        readonly=True,
        related='quote_ref_id.event_date_description',
    )
    quote_ref_venue = fields.Char(
        string='Venue',
        readonly=True,
        related='quote_ref_id.venue_description',
    )
    project_ref_number = fields.Char(
        string='Project Number',
        readonly=True,
        related='project_ref_id.project_number',
    )
    project_ref_name = fields.Char(
        string='Project Name',
        readonly=True,
        related='project_ref_id.name',
    )

    @api.multi
    @api.depends(
        'origin',
        'quote_ref_id',
        'purchase_ref_id',
        'project_ref_id',
    )
    def _compute_quote_ref_id(self):
        for invoice in self:
            print('>>>>>>>>>>>>>>>>>>>>>', invoice._context.get('journal_type'))
            if invoice._context.get('journal_type') == 'sale':
                order_env = self.env['sale.order']
                origin_ref = order_env.search([
                    ('name', '=', invoice.origin)
                ])
                origin_ref = origin_ref.quote_id or False
                if origin_ref:
                    invoice.quote_ref_id = origin_ref
                    project_ref = origin_ref.project_related_id or False
                    if project_ref:
                        invoice.project_ref_id = project_ref
            elif invoice._context.get('journal_type') == 'purchase':
                order_env = self.env['purchase.order']
                origin_ref = order_env.search([
                    ('name', '=', invoice.origin)
                ])
                invoice.purchase_ref_id = origin_ref
                invoice.project_ref_id = origin_ref.project_id
