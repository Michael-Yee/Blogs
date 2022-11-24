---
title: Flask vs FastAPI
author: Michael Yee
published: True
---


# Flask vs FastAPI

In this blog, I will show example code for Flask and FastAPI frameworks to compare and contrast common coding cases

TLDR:

Flask

* Better community support
* Plethora of plugins

FastAPI

* Async capability
* Better developer experience (data validation, serialization/deserialization, automatic documentation, etc..)
* Speed

## Background

Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

# Let's go!

## Installation:

Flask

Terminal: 

```
pip install flask
```

FastAPI

Terminal: 

```
pip install fastapi uvicorn
```

NOTE: FastAPI does not have a built in development server.  We choose to installed `Uvicorn` to solve this problem.

## `Hello World`

Flask

Code:

```
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return {"Hello": "World!"}

if __name__ == "__main__":
    app.run(debug=True)
```

Terminal: 

```
FLASK_APP=hello_world.py 
flask run
```

Note: `debug=True` parameter in app.run() is to enable hot-reloading for development.  Alternatively, you can start the server with hot-reloading directly form the terminal.

```
$ export FLASK_APP=hello_world.py
$ export FLASK_ENV=development
$ flask run
```

FastAPI

```
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World!"}

if __name__ == "__main__":
    uvicorn.run("hello_world:app", reload=True)
```

Terminal: 

```
python hello_world.py
```

Note: `reload=True` parameter in app.run() is to enable hot-reloading for development.  Alternatively, you can start the server directly form the terminal.

```
python hello_world.py --reload
```

## Configuration 

Both Flask and FastAPI provide a few options to store configuration variables. Please refer to the following links:

* Flask - [Configuration Handling](https://flask.palletsprojects.com/en/master/config/)
* FastAPI - [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)

In the following examples, we will place configuration variables in a file. 

Flask

hello_world.py code:

```
from flask import Flask

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")


@app.route("/")
def home():
    return {"Hello": app.config["MESSAGE"]}

if __name__ == "__main__":
    app.run()
```

config.py code:

```
class Config(object):
    DEBUG = False
    MESSAGE = "World!"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    MESSAGE = "Mike!"
```

FastAPI

```
import uvicorn
from functools import lru_cache
from fastapi import Depends, FastAPI
import config


app = FastAPI()


@lru_cache()
def get_settings_development():
    return config.DevelopmentConfig()


@app.get("/")
def home(settings: config.DevelopmentConfig = Depends(get_settings_development)):
    return {"Hello": settings.MESSAGE}

if __name__ == "__main__":
    uvicorn.run("hello_world:app")
```

config.py code:

```
from pydantic import BaseSettings


class Config(BaseSettings):
    DEBUG = False
    MESSAGE = "World!"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    MESSAGE = "Mike!"
```

NOTE: In the FastAPI code, have provided setting from a dependency instead of having a global object.

## HTTP Methods


Flask



