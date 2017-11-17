conf = {
    'door': {
        'value': False,
        'name': 'Open door',
        'type': 'pushbutton',
        'room' : 'holway',
        'device_type' : 'serial',
        'properties' : {
            'communicator': 'bluetooth',
            'send_to_device': 'holway',
            'command': {True: 'O'}
        }
    },
    'homeAlarm': {
        'value': False,
        'name': 'Alarm',
        'type': 'switch',
        'room' : 'general',
        'device_type' : 'action',
        'properties': {}
    },
    'livingCourtainsDwn': {
        'value': False,
        'name': 'Curtains a bit down',
        'type': 'pushbutton',
        'room' : 'living',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L2',
            'command': {True: 'C3|'}
        }
    },
    'livingCourtainsUp': {
        'value': False,
        'name': 'Curtains a bit up',
        'type': 'pushbutton',
        'room' : 'living',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L2',
            'command': {True: 'O3|'}
        }
    },
    'closeAllLights': {
        'value': False,
        'name': 'Close all lights',
        'type': 'pushbutton',
        'room' : 'general',
        'device_type': 'group',
        'properties': {
            'futureState': False,
            'actuators' : ['livingLight', 'bedroomLight', 'kitchenLight', 'holwayLight', 'closetLight', 'balconyLight'],
        }
    },
    'livingCourtains': {
        'value': False,
        'name': 'Curtains',
        'type': 'switch',
        'room' : 'living',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L2',
            'command': {False: 'O90|', True: 'C90|'}
        }
    },
    'livingLight': {
        'value': False,
        'name': 'Main light',
        'type': 'switch',
        'room' : 'living',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '1C|', True: '1O|'}
        }
    },
    'bedroomLight': {
        'value': False,
        'name': 'Main light',
        'type': 'switch',
        'room' : 'bedroom',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '2C|', True: '2O|'}
        }
    },
    'kitchenLight': {
        'value': False,
        'name': 'Main light',
        'type': 'switch',
        'room' : 'kitchen',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '4C|', True: '4O|'}
        }
    },
    'holwayLight': {
        'value': False,
        'name': 'Main light',
        'type': 'switch',
        'room': 'holway',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '3C|', True: '3O|'}
        }
    },
    'closetLight': {
        'value': False,
        'name': 'Main light',
        'type': 'switch',
        'room': 'closet',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '5C|', True: '5O|'}
        }
    },
    'balconyLight': {
        'value': False,
        'name': 'Main light',
        'type': 'switch',
        'room': 'balcony',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '6C|', True: '6O|'}
        }
    },
    'powerSocket1': {
        'value': False,
        'name': 'Power socket (RC)',
        'type': 'switch',
        'room': 'living',
        'device_type': 'serial',
        'properties': {
            'communicator': 'serial',
            'encription': 'aes',
            'send_to_device': 'L1',
            'command': {False: '8C|', True: '8O|'}
        }
    },
    'wemoSwitch1': {
        'value': False,
        'name': 'Power socket (WEMO)',
        'type': 'switch',
        'room': 'holway',
        'device_type': 'wemo',
        'properties': {
            'send_to_device': 'DanSwitch1',
        }
    },
    'zwaveSwitch1': {
        'value': False,
        'name': 'Power socket (ZWAVE)',
        'type': 'switch',
        'room': 'living',
        'device_type': 'zwave',
        'properties': {
            'send_to_device': '0184f904.2.25.1.0',
        }
    },
    'fibaroGreen' : {
        'value': False,
        'name': 'Green color',
        'type': 'dimmer',
        'room': 'living',
        'device_type': 'zwave',
        'properties': {
            'send_to_device': '0184f904.3.26.4.0',
            'max_value': 150
        }
    },
    'fibaroBlue' : {
        'value': False,
        'name': 'Blue color',
        'type': 'dimmer',
        'room': 'living',
        'device_type': 'zwave',
        'properties': {
            'send_to_device': '0184f904.3.26.5.0',
            'max_value': 150
        }
    },
    'fibaroWhite' : {
        'value': False,
        'name': 'White color',
        'type': 'dimmer',
        'room': 'living',
        'device_type': 'zwave',
        'properties': {
            'send_to_device': '0184f904.3.26.6.0',
            'max_value': 150
        }
    },
    'fibaroRed' : {
        'value': False,
        'name': 'Red color',
        'type': 'dimmer',
        'room': 'living',
        'device_type': 'zwave',
        'properties': {
            'send_to_device': '0184f904.3.26.3.0',
            'max_value' : 150
        }
    }
}