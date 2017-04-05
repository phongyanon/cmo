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
        ],
        states={'close': [('readonly', True)]},
    )
    state = fields.Selection(
        selection_add=[
            ('draft','Draft'),
            ('complete', 'Completed'),
            ]
    )
    _defaults = {
        'state': 'draft',
    }

    @api.model
    def create(self, vals):
        vals['project_number'] = self.env['ir.sequence'].get('cmo.project') # create sequence nummber
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
        self.write({'state': 'open'})

    @api.multi
    def action_back_to_draft(self):
        self.write({'state': 'draft'})

    # @api.multi TODO: if all state task are complete then project is complete
    # def write(self, vals):
    #     super().write()
    #     if vals.get('state') == 'Completed':
    #         for task in self:
    #             project = task.project_id
    #             tasks = project.task_ids
    #             not_done_tasks = tasks.filtered(lambda l: l.state != 'Completed')
    #             if not_done_tasks:
    #                 continue
    #             else:
    #                 project.state = 'Completed'

class ProjectTeamMember(models.Model):
    _name = 'project.team.member'
    _description = 'Project Team Member'

    project_ids = fields.Many2one(
        'project.project',
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

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Team Member must be unique!'),
    ]
