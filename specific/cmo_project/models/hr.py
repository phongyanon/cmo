# -*- coding: utf-8 -*-
from openerp import fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"
    _description = "Project Department"

    hr_ids = fields.Many2one(
        'project.department',
        string="Project in Department",
    )
    active = fields.Boolean(
        string='Active',
        default=False,
    )
    show = fields.Boolean(
        string='Show',
        default=False,
    )
