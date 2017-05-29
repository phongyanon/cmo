# -*- coding: utf-8 -*-

from openerp import fields, models, api

class SaleConvenantDescription(models.Model):
    _name = 'sale.convenant.description'

    name = fields.Char(
        string='Name',
        required=True,
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    is_eng = fields.Boolean(
        string='Is English',
        default=True,
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_number = fields.Char(
        string='Project Code',
        readonly=True,
        copy=False,
    )
    project_related_id = fields.Many2one(
        'project.project',
        string='Project',
        states={'done': [('readonly', True)]},
    )
    event_date_description = fields.Char(
        string='Event Date',
        size=250,
        states={'done': [('readonly', True)]},
    )
    venue_description = fields.Char(
        string='Venue',
        size=250,
        states={'done': [('readonly', True)]},
    )
    amount_before_management_fee = fields.Float(
        string="Before Management Fee",
        compute='_compute_before_management_fee',
    )
    payment_term_description = fields.Text(
        string='Payment Term',
        states={'done': [('readonly', True)]},
    )
    convenant_description_eng = fields.Text(
        string='Convenant',
        states={'done': [('readonly', True)]},
        default=lambda self: self._get_eng_convenant(),
    )
    convenant_description_th = fields.Text(
        string=u'เงื่อนไขการยกเลิก',
        states={'done': [('readonly', True)]},
        default=lambda self: self._get_th_convenant(),
    )

    @api.multi
    def _compute_before_management_fee(self):
        total = 0
        for line in self.order_line:
            if line.order_lines_group == 'before':
                total = total + line.price_subtotal
        self.amount_before_management_fee = total

    @api.onchange('project_related_id')
    def _get_project_number(self):
        project = self.env['project.project'].browse(self.project_related_id.id)
        self.project_id = project.analytic_account_id.id
        self.project_number = project.project_number

    @api.multi
    def write(self, vals): # TODO refactor get analytic account by compute field
        self.ensure_one()
        if 'project_related_id' in vals:
            project = self.env['project.project'].browse(vals['project_related_id'])
            self.write({
                'project_id' :  project.analytic_account_id.id,
                'project_number' : project.project_number,
            })
        return super(SaleOrder, self).write(vals)

    @api.model
    def create(self, vals): # TODO refactor get analytic account by compute field
        if 'project_related_id' in vals:
            project = self.env['project.project'].browse(vals['project_related_id'])
            vals['project_id'] = project.analytic_account_id.id
            vals['project_number'] = project.project_number
        return super(SaleOrder, self).create(vals)

    @api.multi
    def _get_eng_convenant(self):
        convenants = self.env['sale.convenant.description'].search([
            ['is_eng', '=', True],
            ['active', '=', True],
        ])
        if convenants:
            return convenants[0].description

    @api.model
    def _get_th_convenant(self):
        convenants = self.env['sale.convenant.description'].search([
            ['is_eng', '=', False],
            ['active', '=', True],
        ])
        if convenants:
            return convenants[0].description


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_lines_group = fields.Selection(
        [('before','Before Management Fee'),
         ('manage_fee','Management and Operation Fee'),
        ],
        string='Group',
        default='before',
    )

    sale_layout_custom_group_id = fields.Many2one(
        'sale_layout.custom_group',
        string='Custom Group',
    )

    sale_order_line_margin = fields.Float(
        string='Margin',
        compute='_get_sale_order_line_margin',
        readonly=True,
    )

    section_code = fields.Selection(
        [('A', 'A'),
         ('B', 'B'),
         ('C', 'C'),
         ('D', 'D'),
         ('E', 'E'),
         ('F', 'F'),
        ],
        string='Section Code',
    )

    @api.multi
    def cal_management_fee(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.cal.manage.fee',
            'src_model': 'sale.order',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'order_line_id': self.id, 'view_id': 'view_sale_management_fee',}
        }

    @api.onchange('price_unit', 'purchase_price')
    def _get_sale_order_line_margin(self):
        margin = self.price_unit - self.purchase_price
        self.sale_order_line_margin = margin

class SaleLayoutCustomGroup(models.Model):
    _name = 'sale_layout.custom_group'

    name = fields.Char(
        string='Name',
        required=True,
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
