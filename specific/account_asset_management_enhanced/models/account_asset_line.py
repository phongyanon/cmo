# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountAssetLine(models.Model):
    _inherit = 'account.asset.line'

    @api.multi
    def write(self, vals):
        write_ctx = self._context
        if 'allow_asset_line_update' in write_ctx:  # prevent maximum recursive
            return super(AccountAssetLine, self).write(vals)

        for dl in self:
            depreciation_line_ids = dl.asset_id.depreciation_line_ids
            if len(depreciation_line_ids) == 1 and dl.type == 'create':
                write_ctx = dict(self._context, allow_asset_line_update=True)

        if 'allow_asset_line_update' not in write_ctx:  # prevent maximum recursive
            return super(AccountAssetLine, self).write(vals)
        res = super(AccountAssetLine, self).with_context(
            write_ctx).write(vals)
        return res
