staticPath = '/home/pi/home-automation/python-server/public'
applicationPort = 8080
credentials = {
    'username' : 'dan',
    'password' : 'cicibici07'
}
btConnections = {
    'bedroom' : '00:14:01:13:16:44',
    'living' : '20:14:12:08:20:45',
    'holway' : '20:14:11:26:10:26',
    'balcony': '98:D3:31:20:A0:51',
    # 'fingerprint': '20:15:12:22:47:86'
}
redisConfig = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
emailConfig = {
    'email': 'dan.ionescu@machteamsoft.ro',
    'password': "Abecedar01",
    'notifiedAddress': 'ionescu.dan84@gmail.com'
}
burglerSoundsFolder = '/home/pi/burglerSounds'