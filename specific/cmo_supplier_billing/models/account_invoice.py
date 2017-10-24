# -*- coding: utf-8 -*-

from openerp import fields, models, api


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
    super_origin = fields.Char(
        string='Super Source Document',
        compute='_compute_super_origin',
        store=True,
    )
    # is_bill = fields.Boolean(
    #     string="Is Billed",
    #     default=False,
    # )

    @api.multi
    def _compute_super_origin(self):
        for invoice in self:
            picking_origin = self.env['stock.picking'].search([
                ('name', '=', invoice.origin),
            ])
            if picking_origin:
                po_origin = self.env['purchase.order'].search([
                    ('name', '=', picking_origin[0].origin),
                ])
                if po_origin:
                    invoice.super_origin = po_origin[0].name
