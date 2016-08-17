web_server = {
    'static_path' : '', # absolute path to static folder ex /home/pi/home-automation/python-server/public
    'application_port' : 8080,
    'cookie_secret' : '' # used for tornado hasing algorithm
}

#home gps coordonates, used for determining if the user is near home or not
home_coordonates = (22.4169649,35.1542889) # replace this with your own

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
burgler_sounds_folder = '' # absoluth path to burgler sounds folder like: /home/pi/burglerSounds