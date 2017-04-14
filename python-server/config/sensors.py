conf = [
    {
        'type' : 'humidity',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('H', False),
        'last_updated' : 0
    },
    {
        'type': 'humidity',
        'value': 0,
        'visible' : ['graphs'],
        'location': 'outside',
        'communication_code': ('H', '1'),
        'last_updated' : 0
    },
    {
        'type' : 'temperature',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('T', False),
        'last_updated': 0
    },
    {
        'type' : 'temperature',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'outside',
        'communication_code': ('T', '1'),
        'last_updated': 0

    },
    {
        'type': 'airPressure',
        'value': 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'outside',
        'communication_code': ('PS', '1'),
        'last_updated': 0
    },
    {
        'type' : 'light',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'living',
        'communication_code': ('L', False),
        'last_updated': 0
    },
    {
        'type': 'light',
        'value': 0,
        'visible': ['graphs'],
        'location': 'outside',
        'communication_code': ('L', '1'),
        'last_updated': 0
    },
    {
        'type': 'voltage',
        'value': 0,
        'visible': ['graphs'],
        'location': 'outside',
        'communication_code': ('V', '1'),
        'last_updated': 0
    },
    {
        'type' : 'rain',
        'value' : 0,
        'visible' : ['graphs'],
        'location': 'outside',
        'communication_code': ('R', '1'),
        'last_updated': 0
    },
    {
        'type' : 'presence',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'holway',
        'communication_code': ('P', False),
        'last_updated': 0
    },
    {
        'type' : 'airPollution',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('Q', False),
        'last_updated': 0
    },
    {
        'type' : 'fingerprint',
        'value' : 0,
        'visible' : [],
        'location': 'outside',
        'communication_code': ('F', False),
        'last_updated': 0
    },
    {
        'type' : 'phoneIsHome',
        'value' : False,
        'visible' : ['homepage'],
        'location': False,
        'communication_code': (False, False),
        'last_updated': 0
    }
]