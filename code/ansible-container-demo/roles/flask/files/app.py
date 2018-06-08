from flask import Flask
from redis import Redis


app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/<name>')
def hello(name):
    last_person = redis.get("last")
    redis.set("last", name)

    if last_person:
        return "Hello {0}! The last human I have seen was {1}.\n".format(name, last_person)
    
    return "Hello {0}! You are my first human I have meet.\n".format(name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
