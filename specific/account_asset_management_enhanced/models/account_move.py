# -*- coding: utf-8 -*-
from openerp import fields, models, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def create(self, vals, **kwargs):
        res = super(AccountMoveLine, self).create(vals, **kwargs)
        if vals.get('asset_id') and vals.get('asset_profile_id'):
            res.asset_id.update({
                'purchase_date': res.date or False,
                'operating_unit_id': vals['operating_unit_id'] or False,
            })
        return res
