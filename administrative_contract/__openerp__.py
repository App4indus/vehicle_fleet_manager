{
    'name': 'Administrative contract',
    'version': '1.0',
    'category': 'Administration',
    'author': 'App4indus',
    'license': 'LGPL',
    'summary': 'Administrative contract management',
    'website': 'https://app4indus.com',
    'module_type': 'base',
    'complexity': 'easy',
    'description': "",
    'depends': ['base', 'account', 'account_openprod'],
    'data': [
        'crons/cron_create_reminder.xml',
        'data/contract_type.xml',
        'security/groups.xml',
        'views/contract.xml',
        'views/calendar_event.xml',
        'views/account_invoice.xml',
        'wizards/add_invoice_to_contract.xml',
        'wizards/quick_create_contract.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'
             ],
    'installable': True
}
