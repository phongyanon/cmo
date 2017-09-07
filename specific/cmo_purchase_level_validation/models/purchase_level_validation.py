# -*- coding: utf-8 -*-

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class PurchaseLevelValidataion(models.Model):
    _name = 'purchase.level.validation'

    level = fields.Integer(
        string='Level',
        required=True,
    )
    limit_amount = fields.Float(
        string='Limit Amount',
        required=True,
    )
    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
    )
    user_ids = fields.Many2many(
        'res.users',
        'res_user_rel', 'validation_id', 'user_id',
        string='Users',
    )


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    level_id = fields.Many2one(
        'purchase.level.validation',
        string='Level Validation',
        track_visibility='onchange',
    )
    approve_ids = fields.Many2many(
        'res.users',
        'res_user_rel', 'purchase_id', 'user_id',
        string='Approval',
        track_visibility='onchange',
    )

    @api.multi
    def action_check_approval(self):
        amount_untaxed = self.amount_untaxed
        target_levels = self.env['purchase.level.validation'].search([
            ('limit_amount', '<=', amount_untaxed),
        ]).sorted(key=lambda r: r.limit_amount)
        print('>>>', target_levels)
        if target_levels:
            if level_id:
                # check approve level
            else:
                # if no have level_id and
            target_limit = max(target_levels.mapped('limit_amount'))
        else:
            return False
        x=1/0
