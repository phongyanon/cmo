# -*- coding: utf-8 -*-
from openerp import models, api


class SaleLayoutCustomGroup(models.Model):
    _inherit = 'sale_layout.custom_group'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context = self._context.copy()
        if context.get('order_ref', False):
            order = self.env['sale.order'].browse(context.get('order_ref'))
            group_ids = order.order_line.mapped(
                'sale_layout_custom_group_id.id')
            args = [('id', 'in', group_ids)] + args
        elif 'order_ref' in context:
            args = [('id', 'in', [])]
        return super(SaleLayoutCustomGroup, self).name_search(
            name, args=args, operator=operator, limit=limit)
