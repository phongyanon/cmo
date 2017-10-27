# -*- coding: utf-8 -*-

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    supplier_billing_id = fields.Many2one(
        'supplier.billing',
        string='Supplier Billing',
        copy=False,
        states={'draft': [('readonly', False)]},
    )
    supplier_billing_number = fields.Char(
        related='supplier_billing_id.number',
        string='Supplier Billing Number',
    )
    # is_bill = fields.Boolean(
    #     string="Is Billed",
    #     default=False,
    # )
