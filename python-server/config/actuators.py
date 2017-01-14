conf = {
    'door': {
        'state': False,
        'type': 'single',
        'device_type': 'door',
        'strategy' : 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'holway',
        'command': {True: 'O'}
    },
    'homeAlarm': {
        'state': False,
        'type': 'bi',
        'device_type': 'action',
        'strategy' : False,
        'communicator': False,
        'send_to_device': False,
        'command': False
    },
    'closeAllLights': {
        'state': False,
        'type': 'single',
        'device_type': 'action',
        'strategy': 'group',
        'futureState': False,
        'actuators' : ['livingLight', 'bedroomLight', 'kitchenLight', 'holwayLight', 'closetLight', 'balconyLight'],
        'communicator': False,
        'send_to_device': False,
        'command': False
    },
    'livingCourtains': {
        'state': False,
        'type': 'bi',
        'device_type': 'courtains',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'balcony',
        'command': {False: 'C50;', True: 'O50;'}
    },
    'livingLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '1C|', True: '1O|'}
    },
    'bedroomLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '2C|', True: '2O|'}
    },
    'kitchenLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '4C|', True: '4O|'}
    },
    'holwayLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '3C|', True: '3O|'}
    },
    'closetLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '5C|', True: '5O|'}
    },
    'balconyLight': {
        'state': False,
        'type': 'bi',
        'device_type': 'light',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '6C|', True: '6O|'}
    },
    'powerSocket1': {
        'state': False,
        'type': 'bi',
        'device_type': 'powerSocket',
        'strategy': 'send',
        'communicator': 'bluetooth',
        'send_to_device': 'living',
        'command': {False: '8C|', True: '8O|'}
    },
    'wemoSwitch1': {
        'state': False,
        'type': 'bi',
        'device_type': 'powerSocket',
        'strategy': 'wemo-switch',
        'communicator': 'wemoSwitch',
        'send_to_device': 'DanSwitch1',
    }
}