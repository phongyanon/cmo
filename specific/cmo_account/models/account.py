# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    quote_ref_id = fields.Many2one(
        'sale.order',
        string='Quotation Ref.',
        readonly=True,
    )
    quote_ref_number = fields.Char(
        string='Quotation Number',
        states={'paid': [('readonly', True)]},
    )
    quote_ref_date = fields.Char(
        string='Quotation Date',
        states={'paid': [('readonly', True)]},
    )
    quote_ref_event_date = fields.Char(
        string='Event Date',
        states={'paid': [('readonly', True)]},
    )
    quote_ref_venue = fields.Char(
        string='Venue',
        states={'paid': [('readonly', True)]},
    )
    project_ref_id = fields.Many2one(
        'project.project',
        string='Project Ref.',
        readonly=True,
    )
    project_ref_number = fields.Char(
        string='Project Number',
        states={'paid': [('readonly', True)]},
    )
    project_ref_name = fields.Char(
        string='Project Name',
        states={'paid': [('readonly', True)]},
    )
    others_note = fields.Text(
        string='Other',
        states={'paid': [('readonly', True)]},
    )

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        order_ref = self.env['sale.order'].search([
            ('name', '=', res.origin)
        ])
        if order_ref:
            quote_id = order_ref.quote_id or False
            if quote_id:
                res.write({
                    'quote_ref_id': quote_id.id,
                    'quote_ref_number': quote_id.name,
                    'quote_ref_date': quote_id.date_order.split(' ')[0],
                    'quote_ref_event_date': quote_id.event_date_description,
                    'quote_ref_venue': quote_id.venue_description,
                    'others_note': quote_id.payment_term_description,
                })
                project_id = quote_id.project_related_id or False
                if project_id:
                    res.write({
                        'project_ref_name': project_id.name,
                        'project_ref_number': project_id.project_number,
                        'project_ref_id': project_id.id,
                    })
        return res

    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None,
                        description=None, journal_id=None):
        res = super(AccountInvoice, self)._prepare_refund(
            invoice, date=date, period_id=period_id,
            description=description, journal_id=journal_id,
        )
        res.update({
            'quote_ref_id': invoice.quote_ref_id.id,
            'quote_ref_number': invoice.quote_ref_number,
            'quote_ref_date': invoice.quote_ref_date,
            'quote_ref_event_date': invoice.quote_ref_event_date,
            'quote_ref_venue': invoice.quote_ref_venue,
            'project_ref_name': invoice.project_ref_name,
            'project_ref_number': invoice.project_ref_number,
            'others_note': invoice.others_note,
        })
        return res
