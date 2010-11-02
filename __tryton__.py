#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Account Netherlands',
    'name_nl_NL': 'Boekhouding Nederland',
    'version': '1.8.0',
    'author': 'NFG',
    'email': 'info@nfg.nl',
    'website': 'http://www.tryton.org/',
    'description': '''Define an account chart template for The Netherlands.
Usefull to create a Dutch account chart with the wizard in
"Financial Management>Configuration>General Account>Create Chart of Account from Template".
''',
    'description_nl_NL': '''Definieert een nederlands grootboekschema, en
    belasting schema.
''',
    'depends': [
        'account',
    ],
    'xml': [
        'account_nl.xml',
    ],
    'translation': [
        'nl_NL.csv',
    ],
}
