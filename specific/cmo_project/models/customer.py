# -*- coding: utf-8 -*-
from openerp import fields, models, api


class SaleCustomer(models.Model):
    _inherit = 'res.partner'
    _description = 'Sale Customer'

    brand_type_id = fields.Many2one(
        'project.brand.type',
        string='Brand type',
    )
    industry_id = fields.Many2one(
        'project.industry',
        string='Industry',
    )
