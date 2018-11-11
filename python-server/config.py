# These settings require that you start / stop the UI and the background service
################################################################################

web_server = {
    'static_path' : '/path/to/static/files', # absolute path to static folder ex: /home/pi/home-automation/python-server/public
    'application_port' : 8080,
    'api_token_secret': 'some_secret_here', # used for secure jwt token generation
    'token_validity_days' : 7 # keeps user authenticated in ui the specified days number
}

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

logging = {
    'log_file': 'log.txt',
    'log_entries': 20000000
}

timezone = 'Europe/Bucharest'

# credentials for logging into the UI
credentials = [
    {
        'username' : '', # your username for web interface
        'password' : '', # your password,
        'fingerprint_code' : '' # your fingerprint code or False if none
    }
]