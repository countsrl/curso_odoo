
{
    'name': 'Estate Account',
    'author': "jasnaykel",
    'category': 'Real Estate',
    'summary': 'Accounting for Real Estate',
    'version': '1.0',
    'license': 'AGPL-3',
    'description': 'Real Estate Manageme',
    'depends':['real_estate','account','base' ], # Dependencia con el módulo de Real Estate
    'data': [
        #'views/estate_property_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}