#-*- coding: utf-8 -*-
 {
    'name': 'Control Colegios',
    'version': '1.0',
    'author': 'Ierai',
    'summary': "Sistema de control de colegios",
    'sequence': 10,
    'description': "Sistema unico para el control de alumnos y material",
    'category': 'Productivity',
    'website': 'https://freeweblearns.blogspot.com',
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        "views/school_view.xml"
    ],
     'installable': True,
     'application': True,
     'auto_install': False,

}