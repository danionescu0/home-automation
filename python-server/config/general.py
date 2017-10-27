web_server = {
    'static_path' : '', # absolute path to static folder ex /home/pi/home-automation/python-server/public
    'application_port' : 8080,
    'cookie_secret' : '', # used for tornado hasing algorithm,
    'api_token_secret': '' # used for secure jwt token generation
}

#home gps coordonates, used for determining if the user is near home or not
home_coordonates = (22.4169649, 35.1542889) # replace this with your own

# credentials for logging into the webapp
credentials = [
    {
        'username' : '', # your username for web interface
        'password' : '', # your password,
        'fingerprint_code' : '' # your fingerprint code or False if none
    }
]

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

email = {
    'email': '', # sender email
    'password': '', # sender password
    'notifiedAddress': '' # receiving email
}

remote_speaker = {
    'host': 'http://your_host_here:80',
    'user': 'test_user',
    'password' : 'test_pass'
}

timezone = 'Europe/Bucharest'

logging = {
    'log_file': 'log.txt',
    'log_entries': 20000000
}

home_defence = {
    'alarm_lock': 360,
    'burgler_lights' : ['livingLight', 'kitchenLight', 'holwayLight'],
    'burgler_time_between_actions' : 3
}

communication = {
    'bluetooth' : {
        'connections' :
            {
                'holway' : '',
                'fingerprint': ''
            }
    },

    'serial' : {
        'port' : '/dev/ttyACM0',
        'baud_rate' : '9600'
    },
    'zwave' : {
        'port' : '/dev/ttyUSB0',
        'openzwave_config_path' : '/your/openzwave/config/path/here'
    },

    'aes_key' : '' # 16 characters key
}