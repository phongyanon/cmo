# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.multi
    def _compute_move_line_check(self):
        for asset in self:
            for line in asset.depreciation_line_ids:
                if line.move_id and line.type != 'depreciate':
                    asset.move_line_check = True
                    continue
