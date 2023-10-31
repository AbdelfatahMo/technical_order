# -*- coding: utf-8 -*-
{
    'name': "technical_order",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '16.0',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base','mail','product','sale'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizard/technical_wizard.xml',
        'views/technical_order.xml',
        'views/res_partner.xml',
        'data/sequence.xml',
        'data/mail_template.xml',
        'reports/report.xml',
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
