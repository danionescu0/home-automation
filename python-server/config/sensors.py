conf = [
    {
        'type' : 'humidity',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('H', False)
    },
    {
        'type': 'humidity',
        'value': 0,
        'visible' : ['graphs'],
        'location': 'outside',
        'communication_code': ('H', '1')
    },
    {
        'type' : 'temperature',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('T', False)
    },
    {
        'type' : 'temperature',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'outside',
        'communication_code': ('T', '1')
    },
    {
        'type': 'airPressure',
        'value': 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'outside',
        'communication_code': ('PS', '1')
    },
    {
        'type' : 'light',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'living',
        'communication_code': ('L', False)
    },
    {
        'type': 'voltage',
        'value': 0,
        'visible': ['graphs'],
        'location': 'outside',
        'communication_code': ('V', '1')
    },
    {
        'type' : 'rain',
        'value' : 0,
        'visible' : [],
        'location': 'outside',
        'communication_code': ('R', False)
    },
    {
        'type' : 'presence',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'holway',
        'communication_code': ('P', False)
    },
    {
        'type' : 'airPollution',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('Q', False)
    },
    {
        'type' : 'fingerprint',
        'value' : 0,
        'visible' : [],
        'location': 'outside',
        'communication_code': ('F', False)
    },
    {
        'type' : 'phoneIsHome',
        'value' : False,
        'visible' : ['homepage'],
        'location': False,
        'communication_code': (False, False)
    }
]