# -*- coding: utf-8 -*-

from openerp import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_number = fields.Char(
        string='Project Code',
        readonly=True,
        copy=False,
    )
    # version = fields.Integer(
    #     string='Version',
    #     size=4,
    #     default=None,
    # )
    project_related_id = fields.Many2one(
        'project.project',
        string='Project',
    )
    version = fields.Char(
        string='Version',
    )
    amount_before_management_fee = fields.Float(
        string="Before Management Fee",
        compute='_compute_before_management_fee',
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
    def write(self, vals):
        self.ensure_one()
        if 'project_related_id' in vals:
            project = self.env['project.project'].browse(vals['project_related_id'])
            self.write({
                'project_id' :  project.analytic_account_id.id,
                'project_number' : project.project_number,
            })
        return super(SaleOrder, self).write(vals)

    @api.model
    def create(self, vals):
        if 'project_related_id' in vals:
            project = self.env['project.project'].browse(vals['project_related_id'])
            vals['project_id'] = project.analytic_account_id.id
            vals['project_number'] = project.project_number
        return super(SaleOrder, self).create(vals)


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

class SaleLayoutCustomGroup(models.Model):
    _name = 'sale_layout.custom_group'

    name = fields.Char(
        string="Name",
        required=True,
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
