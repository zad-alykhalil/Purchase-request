# -*- coding: utf-8 -*-

{
    'name': 'Purchase Request',
    'author': 'Aly Khalil',
    'version': '1.0.0',
    'category': 'Purchase',
    'sequence': -50,
    'summary': 'Purchase Request',
    'description': """Purchase Request System""",
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/reject_view.xml',
        'views/purchase.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
