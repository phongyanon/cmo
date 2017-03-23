# -*- coding: utf-8 -*-
from openerp import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_place = fields.Char(
        string='Project Place',
        states={'close': [('readonly', True)]},
    )
    agency = fields.Many2one(
        'res.partner',
        string="Agency",
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
    # Team tab
    client_service = fields.Many2one(
        'project.department',
        string="Client Service",
        states={'close': [('readonly', True)]},
    )
    designer = fields.Many2one(
        'res.partner',
        string="Designer"
    )
    procurement = fields.Many2one(
        'res.partner',
        string="Procurement"
    )
    production = fields.Many2one(
        'res.partner',
        string="Production"
    )
    project_manager = fields.Many2one(
        'res.partner',
        string="Product Manager"
    )
    creative = fields.Many2one(
        'res.partner',
        string="Creative"
    )
    graphic = fields.Many2one(
        'res.partner',
        string="Graphic"
    )
    producer = fields.Many2one(
        'res.partner',
        string="Produce"
    )
    asst_production = fields.Many2one(
        'res.partner',
        string="Asst. Production"
    )
    # Others Info tab
    project_from = fields.Selection(
        [('unknow', 'Unknow'),
         ('call_in', 'Call in'),
         ('new_prospect', 'New Prospect'),
         ('existing_account', 'Existing Account'),
         ('ceo_office', 'CEO Office'),
         ],
        string='Project From',
        states={'close': [('readonly', True)]},
    )
    project_type = fields.Selection(
        [('unknow', 'Unknow'),
         ('event', 'Event'),
         ('imc_campaign', 'IMC Campaign'),
        ],
        string='Project Type',
        states={'close': [('readonly', True)]},
    )
    department = fields.Many2one(
        'project.department',
        string='Department',
        states={'close': [('readonly', True)]},
    )
    project_budget = fields.Float(
        string='Project Budget'
    )
    estimate_cost = fields.Float(
        string='Estimate cost'
    )
    brief_date = fields.Date(
        string='Brief date',
        default=fields.Date.today
    )
    competitor =fields.Many2many(
        'res.company',
        string="Competitors"
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

class ProjectDepartment(models.Model):
    _name = 'project.department'
    _description = 'Project Department'

    name = fields.Char(
        string='Name',
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=False,
    )
    show = fields.Boolean(
        string='Show',
        default=False,
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Department must be unique!'),
    ]
