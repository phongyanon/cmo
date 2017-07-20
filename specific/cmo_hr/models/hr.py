# -*- coding: utf-8 -*-
import datetime

from openerp import fields, models, api


class HrExpenseExpense(models.Model):
    _inherit = 'hr.expense.expense'

    employee_request_id = fields.Many2one(
        'hr.employee',
        string='Employee Request',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)],
        },
        default=lambda self: self._default_employee_request_id(),
    )
    request_date = fields.Date(
        string='Request Date',
        default=lambda self: fields.Date.context_today(self),
        states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)],
        },
    )
    due_date = fields.Date(
        string='Due Date',
        default=lambda self: fields.Date.context_today(self),
        states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)],
        },
    )
    payment_by = fields.Selection(
        [('cash', 'Cash'),
         ('cashier_cheque', 'Cashier Cheque'),
         ('bank_transfer', 'Bank Transfer'),
         ('ac_payee', 'A/C Payee'),
        ],
        string='Payment By',
    )
    bank_transfer_ref = fields.Text(
        string='Bank Transfer Ref.',
        states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)],
        },
    )
    ac_payee_ref = fields.Text(
        string='A/C Payee Ref.',
        states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)],
        },
    )
    state = fields.Selection(
        selection_add=[
            ('validate', 'Waiting Validate'),
        ],
    )

    @api.multi
    @api.onchange('payment_by')
    def _onchange_payment_by(self):
        self.ensure_one()
        self.bank_transfer_ref = False
        self.ac_payee_ref = False

    @api.multi
    def action_validate(self):
        res = self.write({'state': 'validate'})
        return res

    @api.model
    def _default_employee_request_id(self):
        Employee = self.env['hr.employee']
        employee_request_id = Employee.search([('user_id', '=', self._uid), ])
        return employee_request_id and employee_request_id[0].id or False


class HrExpenseLine(models.Model):
    _inherit = 'hr.expense.line'

    amount_line_untaxed = fields.Float(
        string="Total Untaxed",
        compute='_compute_amount_line_untaxed',
        readonly=True,
    )

    @api.multi
    @api.depends('amount_line_untaxed')
    def _compute_amount_line_untaxed(self):
        for line in self:
            line.amount_line_untaxed = line.unit_amount * line.unit_quantity
