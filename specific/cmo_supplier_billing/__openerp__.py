# -*- coding: utf-8 -*-

{
    'name': "CMO :: Supplier Billing",
    'summary': "",
    'author': "Phongyanon Y.",
    'website': "http://ecosoft.co.th",
    'category': 'Tools',
    "version": "1.0",
    'depends': [
        'account',
    ],
    'data': [
        'data/billing_sequence.xml',
        'security/ir.model.access.csv',
        'views/supplier_billing.xml',
    ],
    'demo': [
    ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
