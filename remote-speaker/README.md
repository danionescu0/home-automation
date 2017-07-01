## Remote speaker

** What is this? **

This is a remote speaker that has the ability to play text to speech. 

** Components **

* linux comatible development board with WIFI access, i've used [C.H.I.P.](https://getchip.com/pages/chip), 
Raspberry pi can be used too.

* speaker

* a power supply with two usb to micro-usb adaptors

* audio cable (male-male)

** Instalation **

* python 2.7x and pip are required
* run pip install -r requirements.txt
* [festival](http://festvox.org/festival/) installed
* to start the service run python server.py

* copy remote-speaker.service to /etc/systemd/system/

* enable service:
````
sudo systemctl enable remote-speaker.service
````

* reboot

* optional, check status:
````
sudo systemctl status remote-speaker.service
````


** Configuration **

In config.py one can change:

port, user and password