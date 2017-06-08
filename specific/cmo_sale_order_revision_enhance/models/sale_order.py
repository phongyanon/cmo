# -*- coding: utf-8 -*-

from openerp import fields, models, api
from openerp.tools.translate import _


class sale_order(models.Model):
    _inherit = "sale.order"

    current_revision_id = fields.Many2one(
        'sale.order',
        string='Current Revision',
        readonly=True,
        copy=True,
    )
    old_revision_ids = fields.One2many(
        'sale.order',
        'current_revision_id',
        string='Old Revision',
        readonly=True,
        context={'active_test': False},
    )
    revision_number = fields.Integer(
        string='Revision',
        copy=False,
    )
    unrevisioned_name = fields.Char(
        string='Order Reference',
        copy=True,
        readonly=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        copy=True,
    )

    _sql_constraints = [
        ('revision_unique',
         'unique(unrevisioned_name, revision_number, company_id)',
         'Order Reference and revision must be unique per Company.'),
    ]

    @api.model
    def create(self, vals):
        if 'unrevisioned_name' not in vals:
            if vals.get('name', '/') == '/':
                seq = self.env['ir.sequence']
                vals['name'] = seq.next_by_code('sale.order') or '/'
            vals['unrevisioned_name'] = vals['name']
        return super(sale_order, self).create(vals)

    @api.multi
    def copy_quotation(self):
        self.ensure_one()
        revision_self = self.with_context(new_sale_revision=True)
        action = super(sale_order, revision_self).copy_quotation()
        old_revision = self.browse(action['res_id'])
        action['res_id'] = self.id
        self.delete_workflow()
        self.create_workflow()
        self.write({'state': 'draft'})
        self.order_line.write({'state': 'draft'})
        # remove old procurements
        self.mapped('order_line.procurement_ids').write(
            {'sale_line_id': False},
        )
        msg = _('New revision created: %s') % self.name
        self.message_post(body=msg)
        old_revision.message_post(body=msg)
        return action

    @api.returns('self', lambda value: value.id)
    @api.multi
    def copy(self, defaults=None):
        context_update = {}
        if not defaults:
            defaults = {}
        if self.env.context.get('new_sale_revision'):
            prev_name = self.name
            if self.current_revision_id:
                current_order = self.env['sale.order'].browse(
                    self.current_revision_id.id)
                revno = current_order.revision_number
                for order in current_order.old_revision_ids:
                    order.write({'current_revision_id': self.id})
                current_order.write({
                    'current_revision_id': self.id,
                    'active': False,
                    'state': 'cancel',
                })
                self.write({
                    'current_revision_id': None,
                    'active': True,
                    'state': 'draft',
                })
                new_revno = self.revision_number
            else:
                revno = self.revision_number
                new_revno = revno
            self.write({
                'revision_number': revno + 1,
                'name': '%s-%02d' % (self.unrevisioned_name, revno + 1),
            })
            context_update = {
                'name': prev_name,
                'revision_number': new_revno,
                'active': False,
                'state': 'cancel',
                'current_revision_id': self.id,
                'unrevisioned_name': self.unrevisioned_name,
            }
            defaults.update(context_update)
        return super(sale_order, self).copy(defaults)

    @api.multi
    def order_revision_tree_view(self):
        self.ensure_one()
        domain = [
            '&', ('current_revision_id', 'like', self.id),
            '&', ('active', '=', False), ('state', '=', 'cancel'),
        ]
        return {
            'name': _('Revision'),
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'views': [[False, "tree"], [False, "form"]],
            'domain': domain,
            'context': "{'active': False}"
        }
