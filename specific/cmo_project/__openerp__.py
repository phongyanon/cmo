# -*- coding: utf-8 -*-
{
    "name": "CMO :: Project Extension",
    "summary": "",
    "version": "1.0",
    "category": "Project",
    "description": """

* Additional fields for project master

    """,
    "website": "http://ecosoft.co.th",
    "author": "Kitti U., Phongyanon Y.",
    "license": "AGPL-3",
    "depends": [
        'project',
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/cmo_project_sequence.xml',
        'data/project_data.xml',
        'data/brand_type_data.xml',
        'data/client_type_data.xml',
        'data/industry_data.xml',
        'data/location_data.xml',
        'data/obligation_data.xml',
        'data/project_from_data.xml',
        'data/project_function_data.xml',
        'data/project_position_data.xml',
        'data/project_type_data.xml',
        'data/tag_type_data.xml',
        'wizard/close_reason_view.xml',
        'wizard/hold_reason_view.xml',
        'views/project_view.xml',
        'views/master_data_view.xml',
        'views/customer_view.xml',
    ],
    "application": False,
    "installable": True,
}
