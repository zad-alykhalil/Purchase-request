# -*- coding: utf-8 -*-

{
    'name': 'Purchase Request',
    'author': 'Aly Khalil',
    'version': '1.0.0',
    'category': 'Purchase',
    'sequence': -50,
    'summary': 'Purchase Request',
    'description': """Purchase Request System""",
    'depends': ['base', 'product', 'sale', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/reject_view.xml',
        'views/purchase_request_view.xml',
        'report/report.xml',
        'report/template_purchase.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
