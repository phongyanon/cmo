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
    quote_ref_number = fields.Char(
        string='Quotation Number',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    quote_ref_date = fields.Datetime(
        string='Quotation Date',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    quote_ref_event_date = fields.Char(
        string='Event Date',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    quote_ref_venue = fields.Char(
        string='Venue',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    project_ref_number = fields.Char(
        string='Project Number',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    project_ref_name = fields.Char(
        string='Project Name',
        readonly=True,
        compute='_compute_quote_ref_id',
    )
    purchase_ref_id = fields.Many2one(
        'purchase.order',
        readonly=True,
        compute='_compute_purchase_ref_id',
    )
    project_ref_id = fields.Many2one(
        'project.project',
        string='Project Ref.',
        compute='_compute_project_ref_id',
    )

    @api.multi
    @api.depends(
        'origin',
        'quote_ref_id',
        'quote_ref_number',
        'quote_ref_date',
        'project_ref_number',
        'project_ref_name',
        'quote_ref_event_date',
        'quote_ref_venue',
    )
    def _compute_quote_ref_id(self):
        for invoice in self:
            quote_ref = self.env['sale.order'].search([
                ('name', '=', invoice.origin)
            ])
            quote_ref = quote_ref.quote_id or False
            if quote_ref:
                invoice.quote_ref_id = quote_ref
                invoice.quote_ref_number = quote_ref.name
                invoice.quote_ref_date = quote_ref.date_order
                invoice.quote_ref_event_date = quote_ref.event_date_description
                invoice.quote_ref_venue = quote_ref.venue_description

                project_ref = quote_ref.project_related_id or False
                if project_ref:
                    invoice.project_ref_number = project_ref.project_number
                    invoice.project_ref_name = project_ref.name

    # @api.multi
    # @api.depends('project_ref_id')
    # def _compute_project_ref_id(self):
    #     for invoice in self:
    #         origin_ref = self.env['sale.order'].search([
    #             ('name', '=', invoice.origin)
    #         ])
    #         invoice.project_ref_id = origin_ref.
