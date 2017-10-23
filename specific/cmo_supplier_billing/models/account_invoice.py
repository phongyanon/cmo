# -*- coding: utf-8 -*-

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    supplier_billing_id = fields.Many2one(
        'supplier.billing',
        string='Supplier Billing',
    )
    supplier_billing_number = fields.Char(
        related='supplier_billing_id.number',
        string='Supplier Billing Number',
    )
    partner_id_name = fields.Char(
        related='partner_id.name',
        string='Supplier',
    )
    # is_bill = fields.Boolean(
    #     string="Is Billed",
    #     default=False,
    # )
