---
title: How to refactor a Flask application to use Blueprints - Part Two
author: Michael Yee
published: True
---


# Overview

Application factory enhances the experience of using blueprints by simplifying the initialization of a Flask project


## What does application factory function do for me?

- Creating the Flask application as an instance of the Flask class
- Configuring the Flask application
- Initializing the extensions to be used
- Registering the Blueprints in the project

## What can I do with this funciton?

- Testing: You can have instances of the application with different settings to test every case.
- Multiple instances: Imagine you want to run different versions of the same application. Of course you could have multiple instances with different configs set up in your webserver, but if you use application factory, you can have multiple instances of the same application running in the same application process.

## The application factory function

The application factory function is created in the ".../project/__init__.py" file. 

```python
   
    #import all the modules!
    from flask import Flask
    from project.retrieval import retrieval_blueprint
    from project.scrape import scrape_blueprint


    # define the application factory function
    def create_app(config_filename=None):
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_pyfile(config_filename)  

        # register all the blueprints
        app.register_blueprint(retrieval_blueprint)
        app.register_blueprint(scrape_blueprint)

        return app

```

The application factory function is used in the ".../main.py" file:

```python

    import app_utils
    from project import create_app
     
    # call the application factory function to construct a Flask application instance using the configuration defined in ".../instance/flask.cfg"
    app = create_app(config_filename="production.cfg")

```

To run the Flask application:

    $ export FLASK_APP=app.py
    $ flask run

# Summary

The application factory function is defined in the ".../project/__init__.py" file and the actual Flask application is then created in ".../app.py".
For more information, please visit:  http://flask.pocoo.org/docs/1.0/patterns/appfactories
