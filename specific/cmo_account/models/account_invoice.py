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
        })
        return res
