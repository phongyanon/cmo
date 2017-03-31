# -*- coding: utf-8 -*-
from openerp import fields, models, api

class ProjectProject(models.Model):
    _inherit = 'project.project'
    # TODO match all selection field with master data
    project_place = fields.Char(
        string='Project Place',
        states={'close': [('readonly', True)]},
    )
    agency = fields.Many2one( # TODO filter res.partner where is agency=1
        'res.partner',
        string="Agency",
        states={'close': [('readonly', True)]},
    )
    brand_type = fields.Many2one(
        'project.brand.type',
        string="Brand type",
        states={'close': [('readonly', True)]},
    )
    industry = fields.Many2one(
        'project.industry',
        string="Industry",
        states={'close':[('readonly', True)]},
    )
    client_type = fields.Many2one(
        'project.client.type',
        string='Client Type',
        states={'close': [('readonly', True)]},
    )
    obligation = fields.Many2one(
        'project.obligation',
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
    location = fields.Many2one(
        'project.location',
        string='Location',
        states={'close': [('readonly', True)]},
    )
    description = fields.Text(
        string='Description',
        states={'close': [('readonly', True)]},
    )
    client_service = fields.Many2one(
        'project.department',
        string="Client Service",
        states={'close': [('readonly', True)]},
    )
    project_from = fields.Many2one(
        'project.from',
        string='Project From',
        states={'close': [('readonly', True)]},
    )
    project_type = fields.Many2one(
        'project.type',
        string='Project Type',
        states={'close': [('readonly', True)]},
    )
    department = fields.Many2one(
        'project.department',
        string='Department',
        states={'close': [('readonly', True)]},
    )
    project_budget = fields.Float(
        string='Project Budget',
        states={'close': [('readonly', True)]},
    )
    actual_price = fields.Float(
        string='Actual Price',
        states={'close': [('readonly', True)]},
    )
    estimate_cost = fields.Float(
        string='Estimate cost',
        states={'close': [('readonly', True)]},
    )
    actual_po = fields.Float(
        string='Actual PO',
        states={'close': [('readonly', True)]},
    )
    remain_advance = fields.Float(
        string='Remain Advance',
        states={'close': [('readonly', True)]},
    )
    expense = fields.Float(
        string='Expense',
        states={'close': [('readonly', True)]},
    )
    brief_date = fields.Date(
        string='Brief date',
        default=fields.Date.today,
        states={'close': [('readonly', True)]},
    )
    competitor =fields.Many2many(
        'res.company',
        string='Competitors',
        states={'close': [('readonly', True)]},
    )
    project_number = fields.Char(
        string='Project Code',
        readonly=True,
        default=lambda self: self.env['ir.sequence'].get('cmo.project'), # create sequence nummber
        states={'close': [('readonly', True)]},
    )
    project_members = fields.One2many(
        'project.team.member',
        'project_ids',
        string='Team Member',
        states={'close': [('readonly', True)]},
    )
    close_reason = fields.Selection([
        ('close', "Closed"),
        ('reject', "Reject"),
        ('lost', "Lost"),
    ], states={'close': [('readonly', True)]},)

    state = fields.Selection(selection_add=[('complete', 'Completed')])
    _defaults = {
        'state': 'draft',
    }

    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        task_obj = self.env['project.task']
        task_list = [
                        {'name': 'ONE'},
                        {'name': 'Billing'},
                        {'name': 'Received'}
                    ]
        for task in task_list:
            task_obj.create({
                            'name': task.get('name', False),
                            'project_id': project.id
                        })
        return project

    @api.multi
    def action_approve(self):
        self.state = 'open'

    @api.multi
    def action_back_to_draft(self):
        self.state = 'draft'

    @api.multi
    def set_done(self, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reason for close project',
            'src_model': 'project.project',
            'res_model': 'project.close.reason',
            'view_mode': 'form',
            'target': 'new',
            'ref': "view_project_close_reason",
        }

class ProjectDepartment(models.Model): # TODO not use, use odoo standard instead.
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

class ProjectTeamMember(models.Model):
    _name = 'project.team.member'
    _description = 'Project Team Member'

    project_ids = fields.Many2one(
        'project.position',
    )
    member_position = fields.Many2one(
        'project.position',
        string='Member Position',
        required=True,
    )
    team_member = fields.Many2one(
        'hr.employee',
        string='Name',
        required=True,
    )
    date_start = fields.Date(
        string='Start',
    )
    date_end = fields.Date(
        string='End date',
    )
