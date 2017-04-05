# -*- coding: utf-8 -*-
from openerp import fields, models, api

class ProjectBrandType(models.Model):
    _name = 'project.brand.type'
    _description = 'Project Brand Type'

    name = fields.Char(
        string='Brand Type',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Brand Type must be unique!'),
    ]

class ProjectClientType(models.Model):
    _name = 'project.client.type'
    _description = 'Project Client Type'

    name = fields.Char(
        string='Client Type',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Client Type must be unique!'),
    ]

class Projectindustry(models.Model):
    _name = 'project.industry'
    _description = 'Project Industry'

    name = fields.Char(
        string='industry',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Industry must be unique!'),
    ]

class ProjectLocation(models.Model):
    _name = 'project.location'
    _description = 'Project Location'

    name = fields.Char(
        string='Location',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Location must be unique!'),
    ]

class ProjectObligation(models.Model):
    _name = 'project.obligation'
    _description = 'Project Obligation'

    name = fields.Char(
        string='Obligation',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Obligation must be unique!'),
    ]

class ProjectFrom(models.Model):
    _name = 'project.from'
    _description = 'Project From'

    name = fields.Char(
        string='Project From',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project From must be unique!'),
    ]

class ProjectFunction(models.Model):
    _name = 'project.function'
    _description = 'Project Function'

    name = fields.Char(
        string='Name',
        required=True,
        size=128,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Function must be unique!'),
    ]

class ProjectPosition(models.Model):
    _name = 'project.position'
    _description = 'Project Position'

    name = fields.Char(
        string='Position',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Position must be unique!'),
    ]


class ProjectType(models.Model):
    _name = 'project.type'
    _description = 'Project Type'

    name = fields.Char(
        string='Project Type',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Position must be unique!'),
    ]


class ProjectDepartment(models.Model): # TODO not use, use odoo standard instead.
    _inherit = 'hr.department'
    _description = 'Project Department'

    active = fields.Boolean(
        string='Active',
        default=False,
    )
    show = fields.Boolean(
        string='Show',
        default=False,
    )
