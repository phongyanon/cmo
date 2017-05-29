# -*- coding: utf-8 -*-
{
    "name": "CMO :: Product Extension",
    "summary": "",
    "version": "1.0",
    "category": "Project",
    "description": """

* Additional fields for product master

    """,
    "website": "http://ecosoft.co.th",
    "author": "Kitti U., Phongyanon Y.",
    "license": "AGPL-3",
    "depends": [
        'product',
        'sale',
        'sale_stock',
        'sale_margin',
        'sale_analytic_plans',
    ],
    "data": [
        'views/product_view.xml',
    ],
    "application": False,
    "installable": True,
}
