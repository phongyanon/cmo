# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one(
        'project.project',
        string='Project Name',
        ondelete='restrict',
    )
    order_ref = fields.Many2one(
        'sale.order',
        string='Quotation Number',
        ondelete='restrict',
    )
    event_date_description = fields.Char(
        string='Event Date',
        size=250,
    )
    venue_description = fields.Char(
        string='Venue',
        size=250,
    )
    po_type_id = fields.Many2one(
        'purchase.order.type.config',
        string='PO Type',
        required=True,
    )
    po_project = fields.Boolean(
        string='PO Project',
        related='po_type_id.po_project',
    )
    approve_ids = fields.Many2one(
        'hr.employee',
        string='PO Approve',
        required=True,
    )
    operating_unit_id = fields.Many2one(
        change_default=True,
    )

    @api.onchange('po_type_id')
    def _onchange_po_type_id(self):
        self.project_id = False
        self.order_ref = False
        self.event_date_description = False
        self.venue_description = False
        self.order_line = False
        self.invoice_method = self.po_type_id and \
            self.po_type_id.invoice_method or False

    @api.onchange('project_id')
    def _onchange_project_id(self):
        self.order_ref = False
        self.event_date_description = False
        self.venue_description = False
        for line in self.order_line:
            line.group_id = False
            line.product_ref = False

    @api.onchange('order_ref')
    def _onchange_order_id(self):
        self.event_date_description = self.order_ref.event_date_description
        self.venue_description = self.order_ref.venue_description
        for line in self.order_line:
            line.group_id = False
            line.product_ref = False

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            ctx = self._context.copy()
            fiscalyear_id = self.env['account.fiscalyear'].find()
            ctx["fiscalyear_id"] = fiscalyear_id
            vals['name'] = self.env['ir.sequence'].\
                with_context(ctx).get('cmo.purchase')
        order = super(PurchaseOrder, self).create(vals)
        order._check_amount_untaxed()
        return order

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        self._check_amount_untaxed()
        return res

    @api.multi
    def _check_amount_untaxed(self):
        for order in self:
            po_project = order.po_type_id and order.po_type_id.po_project \
                or False
            remaining_cost = order.project_id and \
                order.project_id.remaining_cost or False
            if po_project and remaining_cost is not False:
                if order.amount_untaxed > remaining_cost:
                    raise ValidationError(
                        "PO value is over project cost please change value")


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_ref = fields.Many2one(
        'product.product',
        string='Product Ref',
    )
    date_planned = fields.Date(
        required=False,
    )
    group_id = fields.Many2one(
        'sale_layout.custom_group',
        string='Custom Group',
    )

    @api.onchange('group_id')
    def _onchange_group_id(self):
        self.product_ref = False


class PurchaseOrderTypeConfig(models.Model):
    _name = "purchase.order.type.config"

    name = fields.Char(
        string='PO Type',
    )
    category_id = fields.Many2one(
        'product.category',
        string='Internal Category',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    po_project = fields.Boolean(
        string='PO Project',
        default=False,
    )
    invoice_method = fields.Selection(
        [('manual', 'Based on Purchase Order lines'),
         ('order', 'Based on generated draft invoice'),
         ('picking', 'Based on incoming shipments'),
         ('line_percentage', 'Based on line percentage'),
         ('invoice_plan', 'Invoice Plan'), ],
        string='Invoicing Control',
        required=True,
        default='order',
    )
