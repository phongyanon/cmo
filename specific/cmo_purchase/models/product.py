# -*- coding: utf-8 -*-
from openerp import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context = self._context.copy()

        # Search Product Ref from Quotation Number
        if context.get('order_ref', False):
            group_id = context.get('group_id', False)
            order = self.env['sale.order'].browse(context.get('order_ref'))
            product_ids = order.order_line.filtered(
                lambda x: x.sale_layout_custom_group_id.id == group_id) \
                .mapped('product_id.id')
            args = [('id', 'in', product_ids)] + args
        elif 'order_ref' in context:
            args = [('id', 'in', [])]

        # Search products by category
        if context.get('po_type_id', False):
            po_type_id = context.get('po_type_id', [])
            PoTypeConfig = self.env['purchase.order.type.config']
            po_type_config = PoTypeConfig.browse(po_type_id)
            categ_ids = po_type_config.category_id.mapped('id')
            product = self.search([('categ_id', 'in', categ_ids)])
            product_ids = product.mapped('id')
            args = [('id', 'in', product_ids)] + args
        elif 'po_type_id' in context:
            args = [('id', 'in', [])]
        return super(ProductProduct, self).name_search(
            name, args=args, operator=operator, limit=limit)
