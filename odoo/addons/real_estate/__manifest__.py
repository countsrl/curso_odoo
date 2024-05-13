
{
    'name': 'Real Estate',
    'author': "jasnaykel",
    'category': 'Real Estate',
    'version': '1.0',
    'license': 'AGPL-3',
    'description': 'Manage properties for sale and for rent.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
   
           
             'views/estate_menus.xml',
             'views/estate_property_views.xml',
             'views/estate_property_tag.xml',
             'views/estate_property_type.xml',
             'views/estate_property_offer.xml',
             'report/estate_property_templates.xml',
             'report/estate_property_reports.xml',
             'views/assets.xml',

       
    ],
}
