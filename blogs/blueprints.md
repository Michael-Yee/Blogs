---
title: How to refactor a Flask application to use Blueprints - Part One
author: Michael Yee
published: True
---


# Overview

Blueprints encapsulates components of the application by adopting a new folder structure which will aid in maintaining the code base and scales well as we build larger applications.


## What is Flask blueprints?

Think "mini Flask application" when you think of a blueprint.  While not having all the functionallly of a Flask application, blueprints allow you to register routes to them which give you the ability to share elements between them like a common URL prefix, a separate template or static folder.


## Restructuring the application

Sample blueprint folder structure for the Flask application

.
├── app.py # file to start the server
├── app_utils.py # helper functions for app
│
├── instance # configuration files
│ 
├── project # the root folder for all of our resources
│   │ 
│   ├── __init__.py # where we define the app's variables and registering blueprints  
│   │ 
│   ├── templates # templates for ALL other templates to inherit from
│   │   └── base.html
│   │ 
│   ├── retrieval # a folder for the retrieval resource
│   │   ├── __init__.py
│   │   ├── retrieval_utils.py # helper functions for retrieval
│   │   ├── routes.py
│   │   ├── static # storage location for CSS, JS, images, etc...
│   │   └── templates # templates specific to the retrieval resource
│   │       └── retrieval
│   │           └── display.html
│   │ 
│   ├── scrape # a folder for the scrape resource
│   │   ├── __init__.py
│   │   ├── scrape_utils.py
│   │   └── routes.py
│   │
│   └── ...
│   
└── ...

Let us take a look at a single blueprint (retrieval folder), it encapsulates all the components to handle the retrieval functionally of the application (defining routes, generating templates, etc...)

retrieval 
├── __init__.py
├── retrieval_utils.py
├── routes.py
├── static
└── templates 
    └── retrieval
        └── display.html

The recommended naming structure for storing templates is ".../blueprint_name/templates/blueprint_name/". The template directory for each blueprint is added to the search path within your Flask application. With this structure, you can define the templates for each blueprint within the blueprint and still import a base template ".../project/templates/ that is shared by all the blueprints.

In order to create the blueprint, an object of the blueprint class gets instantiated in the __init__.py file:

```python

    """ The retrieval blueprint handles the retrieval functionality for this application"""
    from flask import Blueprint

    # instantiation of the blueprint specifies the name of the blueprint ("retrieval") and it specifies the location of the template files within the blueprint
    retrieval_blueprint = Blueprint('retrieval', __name__, template_folder='templates')

    # imports the routes created in routes.py
    from . import routes

```

The retrieval_blueprint that was created in __init__.py is imported into the routes.py file:

```python

    # imports
    from flask import make_response, render_template
    from http import HTTPStatus
    from . import retrieval_blueprint # this import allows the routes to be specified with "@retrieval_blueprint"
    from .retrieval_utils import get_funny_quote

    # routes
    @retrieval_blueprint.route('/retrieve')
    def retrieve():
        """ this function will retrieve a funny quote and """
        
        return make_response(render_template("display.html", get_funny_quote(), HTTPStatus.OK)

```

# Summary

The blueprints are defined in separate modules in the ".../project" folder
For more information, please visit: http://flask.pocoo.org/docs/1.0/blueprints
