conf = [
    {
        'id' : 'humidity_living',
        'type' : 'humidity',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('H', False),
        'last_updated' : 0
    },
    {
        'id' : 'humidity_outside',
        'type': 'humidity',
        'value': 0,
        'visible' : ['graphs'],
        'location': 'outside',
        'communication_code': ('H', '1'),
        'last_updated' : 0
    },
    {
        'id' : 'temperature_living',
        'type' : 'temperature',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('T', False),
        'last_updated': 0
    },
    {
        'id' : 'temperature_outside',
        'type' : 'temperature',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'outside',
        'communication_code': ('T', '1'),
        'last_updated': 0

    },
    {
        'id' : 'airPressure_outside',
        'type': 'airPressure',
        'value': 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'outside',
        'communication_code': ('PS', '1'),
        'last_updated': 0
    },
    {
        'id' : 'light_living',
        'type' : 'light',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location' : 'living',
        'communication_code': ('L', False),
        'last_updated': 0
    },
    {
        'id' : 'light_outside',
        'type': 'light',
        'value': 0,
        'visible': ['graphs'],
        'location': 'outside',
        'communication_code': ('L', '1'),
        'last_updated': 0
    },
    {
        'id' : 'voltage_outside',
        'type': 'voltage',
        'value': 0,
        'visible': ['graphs'],
        'location': 'outside',
        'communication_code': ('V', '1'),
        'last_updated': 0
    },
    {
        'id' : 'rain_outside',
        'type' : 'rain',
        'value' : 0,
        'visible' : ['graphs'],
        'location': 'outside',
        'communication_code': ('R', '1'),
        'last_updated': 0
    },
    {
        'id' : 'presence_holway',
        'type' : 'presence',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'holway',
        'communication_code': ('P', False),
        'last_updated': 0
    },
    {
        'id' : 'airPollution_living',
        'type' : 'airPollution',
        'value' : 0,
        'visible' : ['graphs', 'homepage'],
        'location': 'living',
        'communication_code': ('Q', False),
        'last_updated': 0
    },
    {
        'id' : 'fingerprint_outside',
        'type' : 'fingerprint',
        'value' : 0,
        'visible' : [],
        'location': 'outside',
        'communication_code': ('F', False),
        'last_updated': 0
    },
    {
        'id' : 'phoneIsHome',
        'type' : 'phoneIsHome',
        'value' : False,
        'visible' : ['homepage'],
        'location': False,
        'communication_code': (False, False),
        'last_updated': 0
    },
    {
        'id' : 'power_holway',
        'type' : 'power',
        'value': 0,
        'visible' : ['graphs'],
        'location': 'holway',
        'communication_code' : ('W', False),
        'last_updated' : 0
    }
]