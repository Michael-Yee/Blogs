from http import HTTPStatus
from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Ping(Resource):
    def get(self):
        response = {"ping": "pong"}
        return response, HTTPStatus.OK


api.add_resource(Ping, "/V1/ping")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
