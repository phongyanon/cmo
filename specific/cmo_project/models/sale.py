# -*- coding: utf-8 -*-

from openerp import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    version = fields.Integer(
        string='Version',
        size=4,
        default=None,
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    order_lines_level = fields.Selection(
        [('A', 'A'),
         ('B', 'B'),
         ('C', 'C'),
         ('D', 'D'),
         ('E', 'E'),
         ('F', 'F'),
        ],
        string='Level',
        states={'close': [('readonly', True)]},
    )
