# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.exceptions import ValidationError
# TODO: foreign key use, idex and ondelete


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_place = fields.Char(
        string='Project Place',
        states={'close': [('readonly', True)]}
    )
    agency_partner_id = fields.Many2one(
        'res.partner',
        string='Agency',
        states={'close': [('readonly', True)]},
        domain=[('category_id', 'like', 'Agency'), ],
    )
    brand_type_id = fields.Many2one(
        'project.brand.type',
        string='Brand type',
        related='partner_id.brand_type_id',
        states={'close': [('readonly', True)]},
        store=True,
    )
    industry_id = fields.Many2one(
        'project.industry',
        string='Industry',
        related='partner_id.industry_id',
        states={'close':[('readonly', True)]},
        store=True,
    )
    client_type_id = fields.Many2one(
        'project.client.type',
        string='Client Type',
        states={'close': [('readonly', True)]},
    )
    obligation_id = fields.Many2one(
        'project.obligation',
        string='Obligation',
        states={'close': [('readonly', True)]},
    )
    function_id = fields.Many2one(
        'project.function',
        string='Function',
        states={'close': [('readonly', True)]},
    )
    location_id = fields.Many2one(
        'project.location',
        string='Location',
        states={'close': [('readonly', True)]},
    )
    description = fields.Text(
        string='Description',
        states={'close': [('readonly', True)]},
    )
    project_from_id = fields.Many2one(
        'project.from',
        string='Project From',
        states={'close': [('readonly', True)]},
    )
    project_type_id = fields.Many2one(
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
        string='Estimate Cost',
        states={'close': [('readonly', True)]},
    )
    pre_cost = fields.Float(
        string='Pre-Project',
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
        string='Brief Date',
        default=fields.Date.today,
        states={'close': [('readonly', True)]},
    )
    date = fields.Date(
        default=fields.Date.today,
        states={'close': [('readonly', True)]},
    )
    competitor_ids = fields.Many2many(
        'project.competitor',
        'res_competitor_rel', 'project_id', 'competitor_id',
        string='Competitors',
        states={'close': [('readonly', True)]},
    )
    project_number = fields.Char(
        string='Project Code',
        readonly=True,
        states={'close': [('readonly', True)]},
        copy=False,
    )
    project_member_ids = fields.One2many(
        'project.team.member',
        'project_id',
        string='Team Member',
        states={'close': [('readonly', True)]},
    )
    close_reason = fields.Selection(
        [('close', 'Completed'),
         ('reject', 'Reject'),
         ('lost', 'Lost'),
         ('cancel', 'Cancelled'),
         ('terminate', 'Terminated'),
        ],
        string='Close Reason',
        states={'close': [('readonly', True)]},
    )
    department_id = fields.Many2one( # no use
        'hr.department',
        string='Department',
        states={'close': [('readonly', True)]},
    )
    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=lambda self: self.env.user.default_operating_unit_id,
        states={'close': [('readonly', True)]},
    )
    state = fields.Selection(
        [('template', 'Template'),
         ('draft','Draft'),
         ('validate', 'Validated'),
         ('open','In Progress'),
         ('ready_billing', 'Ready to Billing'),
         ('invoices', 'Invoices'),
         ('received', 'Received'),
         ('cancelled', 'Cancelled'),
         ('pending','Pending'),
         ('close','Completed'), ],
         string='Status',
         required=True,
         copy=False,
         default='draft',
    )
    latest_state = fields.Char(
        string='Latest State',
    )
    lost_reason = fields.Many2one(
        'project.lost.reason',
        string='Lost Reason',
    )
    lost_by = fields.Many2one(
        'res.partner',
        string='Lost By',
        domain=[('category_id', 'like', 'Competitor'), ],
    )
    reject_reason = fields.Many2one(
        'project.reject.reason',
        string='Reject Reason',
    )
    hold_reason = fields.Text(
        string='Hold Reason',
        states={'close': [('readonly', True)]},
    )
    assign_id = fields.Many2one(
        'res.users',
        string='Assign to',
        domain=[('default_operating_unit_id', 'like', 'Accounting & Finance'), ],
        states={'close': [('readonly', True)]},
    )
    assign_description = fields.Text(
        string='Description',
        states={'close': [('readonly', True)]},
    )

    _defaults = {
        'use_tasks': False
    }
    # TODO create tab to show invoices of project.
    # invoice_ids = fields.Many2many(
    #     'account.invoice',
    #     string='Invoices',
    #     compute='_compute_invoice_ids',
    #     help="This field show invoices related to this project",
    # )
    #
    # @api.multi
    # @api.depends()
    # def _compute_invoice_ids(self):
    #     self.invoice_ids = []

    @api.model
    def create(self, vals):
        if vals.get('project_number', '/') == '/':
            vals['project_number'] = self.env['ir.sequence'].get('cmo.project') # create sequence number
        project = super(ProjectProject, self).create(vals)
        return project

    @api.multi
    def write(self, vals):
        if ('state' in vals) and \
           (vals['state'] != 'pending') and \
           (vals['state'] != 'close'):
           vals['latest_state'] = vals['state']
        return super(ProjectProject, self).write(vals)

    @api.multi
    def action_validate(self):
        res = self.write({'state':'validate'})
        return res

    @api.multi
    def action_approve(self):
        res = self.write({'state': 'open'})
        return res

    @api.multi
    def action_back_to_draft(self):
        res = self.write({'state': 'draft'})
        return res

    @api.multi
    def action_invoices(self):
        res = self.write({'state': 'invoices'})
        return res

    @api.multi
    def action_received(self):
        res = self.write({'state': 'received'})
        return res

    @api.multi
    def action_ready_billing(self):
        res = self.write({'state': 'ready_billing'})
        return res

    @api.multi
    def action_back_to_open(self):
        res = self.write({'state': 'open'})
        return res

    @api.multi
    def action_released(self):
        if self.latest_state:
            res = self.write({'state':self.latest_state})
        else:
            res = self.write({'state':'open'})
        self.write({'close_reason':None})
        return res

    @api.multi
    @api.constrains('brief_date', 'date')
    def _check_brief_dates(self):
        self.ensure_one()
        if self.brief_date > self.date:
            return ValidationError("project brief-date must be lower than project end-date.")


class ProjectTeamMember(models.Model):
    _name = 'project.team.member'
    _description = 'Project Team Member'
    _rec_name = 'employee_id'

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        ondelete='cascade',
        index=True,
    )
    position_id = fields.Many2one(
        'project.position',
        string='Member Position',
        required=True,
    )
    employee_id = fields.Many2one(
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
    remark = fields.Text(
        string="Remark"
    )


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

class ProjectIndustry(models.Model):
    _name = 'project.industry'
    _description = 'Project Industry'

    name = fields.Char(
        string='Industry',
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

class ProjectCompetitor(models.Model):
    _name = 'project.competitor'
    _description = 'Project Competitor'

    name = fields.Char(
        string='Name',
    )
    company = fields.Char(
        string='Company',
        required=True,
    )
    remark = fields.Text(
        string='Remark',
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Project Lost by must be unique!'),
    ]

class ProjectLostReason(models.Model):
    _name = 'project.lost.reason'
    _description = 'Project Lost Reason'

    name = fields.Char(
        string='Reason',
        required=True,
    )


class ProjectRejectReason(models.Model):
    _name = 'project.reject.reason'
    _description = 'Project Reject Reason'

    name = fields.Char(
        string='Reason',
        required=True,
    )
