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
        copy=False,
    )
    approval_ids = fields.Many2many(
        'res.users',
        'res_approval_rel', 'purchase_id', 'user_id',
        string='Approval',
        track_visibility='onchange',
        copy=False,
    )
    approve_level = fields.Char(
        string='Approve Level ',
        compute='_compute_approve_level',
    )

    @api.depends('level_id', 'approve_level')
    def _compute_approve_level(self):
        for order in self:
            if order.level_id:
                order.approve_level = str(order.level_id.level)

    @api.multi
    def action_check_approval(self):
        amount_untaxed = self.amount_untaxed
        target_levels = self.env['purchase.level.validation'].search([
            ('operating_unit_id', 'in',
                self.env.user.operating_unit_ids.mapped('id')),
            ('limit_amount', '<=', amount_untaxed),
        ]).sorted(key=lambda r: r.level)
        if self.approval_ids and self.env.user not in self.approval_ids:
            raise ValidationError(_("Your user is not allow to "
                                    "approve this document."))
        if target_levels:
            if self.level_id:
                min_level = min(filter(
                        lambda r: r >= self.level_id.level,
                        target_levels.mapped('level')))
                target_level = target_levels.filtered(
                    lambda r: r.level == min_level + 1
                )
                if target_level:
                    self.write({
                        'level_id': target_level.id,
                        'approval_ids': [
                            (6, 0, target_level.user_ids.mapped('id'))
                        ],
                    })
                else:
                    self.write({
                        'level_id': False,
                        'approval_ids': False,
                    })
            else:
                if not self.level_id and not self.approval_ids:
                    target_level = target_levels.filtered(
                        lambda r: r.level == min(target_levels.mapped('level'))
                    )
                    self.write({
                        'level_id': target_level.id,
                        'approval_ids': [
                            (6, 0, target_level.user_ids.mapped('id'))
                        ],
                    })
        return True
