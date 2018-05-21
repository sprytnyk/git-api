import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

from core import settings
from core.celery import FlaskCelery
from core.response import make_json_response

api = Api(prefix='/api')
api.representations['application/json'] = make_json_response
celery = FlaskCelery()
db = MongoEngine()


def create_app():
    """
    Create a Flask app & other stuff with the specific context, that depends
    on the environment.
    """
    app = Flask(__name__)

    # Provide ENV-specific settings.
    environment = os.environ.get('APP_ENV', 'dev')
    environments = {
        'dev': settings.Dev
    }
    app.config.from_object(environments[environment])

    # Initialize external extensions with the app context.
    celery.init_app(app)
    db.init_app(app)

    # Hook up resources and the API extension.
    from app.v1.resources import (
        RepositoriesResource,
        UploadRepositoriesResource
    )
    api.add_resource(RepositoriesResource, '/v1/repositories/')
    api.add_resource(UploadRepositoriesResource, '/v1/upload-repositories/')
    # Circle import workaround.
    api.init_app(app)

    return app
