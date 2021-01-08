# -*- coding: utf-8 -*-
{
    'name': "om_hospital",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filte2021r modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/data.xml',
        'data/mail_template.xml',
        'wizards/create_appointment.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'security/security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
