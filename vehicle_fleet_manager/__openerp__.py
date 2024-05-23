{
    'name': 'Vehicle fleet manager',
    'version': '1.0',
    'category': 'Administration',
    'author': 'Jérôme Botreau (App4indus)',
    'license': 'LGPL',
    'summary': 'Vehicle fleet manager',
    'website': 'https://app4indus.com',
    'module_type': 'base',
    'complexity': 'easy',
    'description': "",
    'depends': ['base', 'administrative_contract'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/vehicle_manufacturer.xml',
        'data/vehicle_type.xml',
        'views/contract.xml',
        'views/vehicle.xml',
        'views/vehicle_model.xml',
        'views/vehicle_manufacturer.xml',
        'views/vehicle_fine.xml',
        'views/vehicle_accident.xml',
        'views/vehicle_use.xml',
        'views/vehicle_intervention.xml',
        'wizards/vehicle_quick_create.xml',
        'wizards/accident_quick_create.xml',
        'wizards/intervention_quick_create.xml',
        'wizards/fine_quick_create.xml',
        'wizards/vehicle_odometer_update.xml',
        'wizards/vehicle_quick_request_use.xml',
        'views/menu.xml',
        'crons/cron_generate_contract_costs.xml',
        'assets/assets.xml'
             ],
    'installable': True
}
