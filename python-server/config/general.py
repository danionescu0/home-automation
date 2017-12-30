web_server = {
    'static_path' : '', # absolute path to static folder ex /home/pi/home-automation/python-server/public
    'application_port' : 8080,
    'api_token_secret': '' # used for secure jwt token generation
}

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

timezone = 'Europe/Bucharest'

logging = {
    'log_file': 'log.txt',
    'log_entries': 20000000
}

#home gps coordonates, used for determining if the user is near home or not
home_coordonates = (22.4169649, 35.1542889) # replace this with your own

remote_speaker = {
    'host': 'http://ip',
    'user': 'test_user',
    'password' : 'test_pass'
}

# credentials for logging into the webapp
credentials = [
    {
        'username' : '', # your username for web interface
        'password' : '', # your password,
        'fingerprint_code' : '' # your fingerprint code or False if none
    }
]

communication = {
    'aes_key' : '' # 16 characters key
}