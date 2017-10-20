# -*- coding: utf-8 -*-

from openerp import fields, models, api


class SupplierBilling(models.Model):
    _name = 'supplier.billing'
    _order = 'date desc, id desc'

    number = fields.Char(
        string='Number',
        size=32,
        readonly=True,
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Supplier',
        domain=[('supplier', '=', True), ],
        states={'billed': [('readonly', True)]},
        required=True,
    )
    date = fields.Date(
        string='Billing Date',
        states={'billed': [('readonly', True)]},
        default=lambda self: fields.Date.context_today(self),
    )
    due_date = fields.Date(
        string='Due Date',
        states={'billed': [('readonly', True)]},
        default=lambda self: fields.Date.context_today(self),
        required=True,
    )
    invoice_ids = fields.One2many(
        'account.invoice',
        'supplier_billing_id',
        states={'billed': [('readonly', True)]},
        strgin='Invoices',
    )
    invoice_related_count = fields.Integer(
        string='# of Invoice',
        compute='_compute_invoice_related_count',
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('billed', 'Billed'),
         ('cancel', 'Cancelled')
         ],
        string='Status',
        required=True,
        copy=False,
        default='draft',
    )

    @api.multi
    @api.depends('invoice_ids')
    def _compute_invoice_related_count(self):
        for billing in self:
            invoice_ids = self.env['account.invoice'].search([
                ('id', 'in', billing.invoice_ids.ids)
            ])
            billing.invoice_related_count = len(invoice_ids)

    @api.multi
    def invoice_relate_billing_tree_view(self):
        self.ensure_one()
        action = self.env.ref('account.action_invoice_tree1')
        result = action.read()[0]
        result.update({'domain': [('id', 'in', self.invoice_ids.ids)]})
        return result

    @api.multi
    def action_billed(self):
        self.ensure_one()
        ctx = self._context.copy()
        current_date = fields.Date.context_today(self)
        fiscalyear_id = self.env['account.fiscalyear'].find(dt=current_date)
        ctx["fiscalyear_id"] = fiscalyear_id
        billing_number = self.env['ir.sequence']\
            .with_context(ctx).get('supplier.billing')
        res = self.write({
            'state': 'billed',
            'number': billing_number,
        })

        if self.invoice_ids:
            for invoice in self.invoice_ids:
                invoice.update({'date_due': self.due_date})
        return res

    @api.multi
    def action_cancel(self):
        res = self.write({'state': 'cancel'})
        if self.invoice_ids:
            for invoice in self.invoice_ids:
                invoice.update({
                    'date_due': False,
                    'supplier_billing_id': False,
                })
        return res
