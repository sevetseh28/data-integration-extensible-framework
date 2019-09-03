"""
This file contains all the tags that must be used by the framework
Each tag has its own semantics which should be explained here
"""

############## ADDRESS ##############
LQ = {
    'id': 'LQ',
    'description': 'Locality qualifier word',
    'component': 'Address'
}
LN = {
    'id': 'LN',
    'description': 'Locality (town, suburb) name',
    'component': 'Address'
}
TR = {
    'id': 'TR',
    'description': 'Territory (town, suburb) name',
    'component': 'Address'
}
CR = {
    'id': 'CR',
    'description': 'Country name',
    'component': 'Address'
}
IT = {
    'id': 'IT',
    'description': 'Institution type',
    'component': 'Address'
}
PA = {
    'id': 'PA',
    'description': 'Postal address type',
    'component': 'Address'
}
PC = {
    'id': 'PC',
    'description': 'Postcode (zipcode)',
    'component': 'Address'
}
N4 = {
    'id': 'N4',
    'description': 'Numbers with four digits',
    'component': 'Address'
}

N34 = {
    'id': 'N34',
    'description': 'Number between 3 and 4 digits',
    'component': 'Address'
}

UT = {
    'id': 'UT',
    'description': 'Unit type (e.g. flat or apartment)',
    'component': 'Address'
}

WN = {
    'id': 'WN',
    'description': 'Wayfare (street) name',
    'component': 'Address'
}

WT = {
    'id': 'WT',
    'description': 'Wayfare (street) type (e.g. road or place)',
    'component': 'Address'
}

############## NAME ##############
TI = {
    'id': 'TI',
    'description': 'Title word (e.g. ms, mrs, mr, dr)',
    'component': 'Name'
}

SN = {
    'id': 'SN',
    'description': 'Surname',
    'component': 'Name'
}

GN = {
    'id': 'GN',
    'description': 'Given name',
    'component': 'Name'
}

GF = {
    'id': 'GF',
    'description': 'Female given name',
    'component': 'Name'
}

GM = {
    'id': 'GM',
    'description': 'Male given name',
    'component': 'Name'
}

PR = {
    'id': 'PR',
    'description': 'Name prefix',
    'component': 'Name'
}

SP = {
    'id': 'SP',
    'description': 'Name separators and qualifiers (e.g. aka or and)',
    'component': 'Name'
}

BO = {
    'id': 'BO',
    'description': '"baby of" and similar values',
    'component': 'Name'
}

NE = {
    'id': 'NE',
    'description': '"nee", "born as" or similar values',
    'component': 'Name'
}

II = {
    'id': 'II',
    'description': 'Initials (one letter token)',
    'component': 'Name'
}

############## ADDRESS / NAME ##############
ST = {
    'id': 'ST',
    'description': 'Saint names (e.g. "saint george" or "san angelo")',
    'component': 'Address/name'
}

CO = {
    'id': 'CO',
    'description': 'Comma, semi-colon, colon',
    'component': 'Address/name'
}

SL = {
    'id': 'SL',
    'description': 'Slash "/" and back-slash "\\"',
    'component': 'Address/name'
}

NU = {
    'id': 'NU',
    'description': 'Other numbers',
    'component': 'Address/name'
}

AN = {
    'id': 'AN',
    'description': 'Alphanumeric tokens',
    'component': 'Address/name'
}

VB = {
    'id': 'VB',
    'description': 'Brackets, braces, quotes',
    'component': 'Address/name'
}

HY = {
    'id': 'HY',
    'description': 'Hyphen "-"',
    'component': 'Address/name'
}

RU = {
    'id': 'RU',
    'description': 'Rubbish (for tokens to be removed)',
    'component': 'Address/name'
}

UN = {
    'id': 'UN',
    'description': 'Unknown (none of the above)',
    'component': 'Address/name'
}
