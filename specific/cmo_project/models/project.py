# -*- coding: utf-8 -*-
from openerp import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_place = fields.Char(
        string='Project Place',
        states={'close': [('readonly', True)]},
    )
    client_type = fields.Selection(
        [('unknown', 'Unknown'),
         ('government', 'Government'),
         ('private_agency', 'Private Sector (Agency)'),
         ('private_direct', 'Private Sector (Direct)'),
         ],
        string='Client Type',
        states={'close': [('readonly', True)]},
    )
    obligation = fields.Selection(
        [('corporate', 'Corporate'),
         ('sale', 'Sales'),
         ('crm', 'CSR'),
         ('csr', 'CSR'),
         ],
        string='Obligation',
        states={'close': [('readonly', True)]},
    )
    function_id = fields.Many2one(
        'project.function',
        string='Function',
        states={'close': [('readonly', True)]},
    )
    lead_source = fields.Selection(
        [('compaign', 'Campaign'),
         ('cold_call', 'Cold Call'),
         ('comference', 'Conference'),
         ('direct_mail', 'Direct Mail'),
         ('email', 'Email'),
         ('employee', 'Employee'),
         ('existing_customer', 'Existing Customer'),
         ('other', 'Others'),
         ('partner', 'Partner'),
         ('campaign', 'Campaign'),
         ],
        string='Lead Source',
        states={'close': [('readonly', True)]},
    )
    location = fields.Selection(
        [('local', 'Local'),
         ('regional', 'Regional'),
         ('international', 'International'),
         ],
        string='Location',
        states={'close': [('readonly', True)]},
    )
    description = fields.Text(
        string='Description',
    )


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
