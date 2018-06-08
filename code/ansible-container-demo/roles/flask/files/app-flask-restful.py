from flask import Flask
from flask_restful import Api, Resource
from redis import Redis


app = Flask(__name__)
api = Api(app)
redis = Redis(host='redis', port=6379)


class Hello(Resource):
    """ Simple hello endpoint"""

    def get(self, name):
        last_person = redis.get("last")
        redis.set("last", name)

        if last_person:
            return "Hello {0}! The last human I have seen was {1}.\n".format(name, last_person)
        
        return "Hello {0}! You are my first human I have meet.\n".format(name)


api.add_resource(Hello, "/<name>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
