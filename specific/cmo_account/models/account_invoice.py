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
        related='quote_ref_id.name',
        string='Quotation Number',
        states={'paid': [('readonly', True)]},
    )
    quote_ref_date = fields.Char(
        string='Quotation Date',
        states={'paid': [('readonly', True)]},
    )
    quote_ref_event_date = fields.Char(
        related='quote_ref_id.event_date_description',
        string='Event Date',
        states={'paid': [('readonly', True)]},
    )
    quote_ref_venue = fields.Char(
        related='quote_ref_id.venue_description',
        string='Venue',
        states={'paid': [('readonly', True)]},
    )
    project_ref_id = fields.Many2one(
         'project.project',
         string='Project Ref.',
         readonly=True,
     )
    project_ref_number = fields.Char(
        related='project_ref_id.project_number',
        string='Project Number',
        states={'paid': [('readonly', True)]},
    )
    project_ref_name = fields.Char(
        related='project_ref_id.name',
        string='Project Name',
        states={'paid': [('readonly', True)]},
    )
    others_note = fields.Text(
        related='quote_ref_id.payment_term_description',
        string='Other',
        states={'paid': [('readonly', True)]},
    )
    project_note = fields.Char(
        string='Description',
        states={'paid': [('readonly', True)]},
     )

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
