## User interface with ReactJs and Core UI

This UI is powered by [CoreUI](http://coreui.io/)


Configuration:

Edit config.js and set the api endpoint 
````
const API_ENDPOINT = 'your_enpoint_here'
````

Install dependencies:
````
npm install

````

Run development server:
````
npm start
````


Run production server:

````
npm build
````

This creates ./build folder whick contains runnable index.html

If you've build the project on your local machine, copy them on the remote machine ( ex: raspberry pi ) to the 
./python-server/public folder.

Then modifiy web_server configuration from config.py which is located in ./python-server/config/general.py

````
....
web_server = {
    'static_path' : '/path/to/static/files', # absolute path to static folder ex: /home/pi/home-automation/python-server/public
    ....
}
...
````

