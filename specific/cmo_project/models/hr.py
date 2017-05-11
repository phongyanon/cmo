# -*- coding: utf-8 -*-
from openerp import fields, models


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    active = fields.Boolean(
        string='Active',
        default=False,
    )
    show = fields.Boolean(
        string='Show',
        default=False,
    )
