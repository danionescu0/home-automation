conf = {
    'door': {
        'state': False,
        'type': 'single',
        'device_type': 'door',
        'communicator': 'bluetooth',
        'send_to_device': 'holway',
        'command': {True: 'O'}
    },
    'homeAlarm': {
        'state': False,
        'type': 'bi',
        'device_type': 'action',
        'communicator': 'bluetooth',
        'send_to_device': False,
        'command': False
    },
    'livingCourtains': {
        'state': False,
        'type': 'bi',
        'device_type': 'courtains',
        'communicator': 'bluetooth',
        'send_to_device': 'balcony',
        'command': {False: '0', True: '1'}
    },
    'closeAllLights': {
        'state': False,
        'type': 'single',
        'device_type': 'action',
        'communicator': 'bluetooth',
        'send_to_device': False,
        'command': False
    },
    'livingLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '1C|', True: '1O|'}
    },
    'bedroomLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '2C|', True: '2O|'}
    },
    'kitchenLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '4C|', True: '4O|'}
    },
    'holwayLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '3C|', True: '3O|'}
    },
    'closetLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '5C|', True: '5O|'}
    },
    'balconyLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '6C|', True: '6O|'}
    },
    'powerSocket1': {
        'state': False,
        'type': 'bi',
        'device_type': 'powerSocket',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '8C|', True: '8O|'}
    }
}