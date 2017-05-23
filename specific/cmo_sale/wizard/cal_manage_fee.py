# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SaleCalManageFee(models.TransientModel):
    _name = 'sale.cal.manage.fee'

    percent_rate = fields.Float(
        string="Rate",
        default=lambda r: 12,
    )

    @api.multi
    def calculate_management_fee(self):
        self.ensure_one()
        order_line = self.env['sale.order.line'].browse(self._context['order_line_id'])
        quote = self.env['sale.order'].browse(order_line.order_id.id)
        fee = quote.amount_before_management_fee * self.percent_rate / 100
        order_line.write({'price_unit': fee})
        return {'type': 'ir.actions.act_window_close'}
