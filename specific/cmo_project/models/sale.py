# -*- coding: utf-8 -*-

from openerp import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_number = fields.Char(
        string='Project Code',
        readonly=True,
        states={'close': [('readonly', True)]},
        # compute="_get_project_number",
        copy=False,
    )
    # version = fields.Integer(
    #     string='Version',
    #     size=4,
    #     default=None,
    # )
    version = fields.Char(
        string='Version',
    )

    # @api.multi
    # def _get_project_number(self):
    #     print(">>>>>>>>>>>>>>>> Get project Number")
    #     for quote in self:
    #         print(quote)
    #         if quote.project_id:
    #             print(quote.project_id)
    #             project = self.env['project.project'].search(analytic_account_id=quote.project_id)
    #             self.write({'project_number':project.project_number})

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_lines_group = fields.Selection(
        [('before','Before Management Fee'),
         ('manage_fee','Management and Operation Fee'),
        ],
        string='Group',
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


class SaleLayoutCustomGroup(models.Model):
    _name = 'sale_layout.custom_group'

    name = fields.Char(
        string="Name",
        required=True,
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
