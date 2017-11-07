import os
from datetime import datetime
from datetime import timedelta

import jwt
from flask import Flask, request, Response


class JwtTokenFactory:
    def __init__(self, jwt_secret: str) -> None:
        self.__jwt_secret = jwt_secret

    def create(self, userid: str) -> str:
        payload = {
            'userid': userid,
            'exp': datetime.utcnow() + timedelta(days=1)
        }

        return jwt.encode(payload, self.__jwt_secret, algorithm='HS256')



token_factory = JwtTokenFactory('cici')
app = Flask(__name__)

@app.route("/api/rooms", methods=["GET"])
def add_user():
    response = '[{"id" : 1, "name": "Living room", "sensors" : [{"type" : "power", "name": "Power 1", "value":230}, {"type" : "temperature", "name": "Temp sensor", "value":20}], "actuators": [{"type" : "switch", "name" : "Main Light switch", "value" : true}, {"type" : "switch", "name" : "Courtains", "value" : false}, {"type" : "pushbutton", "name" : "Courtains nodge down"}]}]'

    return Response(response, status=200, mimetype='application/json')

@app.route("/auth", methods=["POST"])
def auth():
    return Response(token_factory.create("4"), status=200, mimetype='application/json')


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8082))
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=port)