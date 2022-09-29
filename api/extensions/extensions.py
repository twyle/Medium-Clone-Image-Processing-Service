from flask_cors import CORS
from flasgger import LazyString, Swagger
from flask import request
import boto3
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery

load_dotenv()

cors = CORS()
db = SQLAlchemy()
ma = Marshmallow()

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
   aws_secret_access_key=os.environ['AWS_ACCESS_SECRET']
)

migrate = Migrate()

def make_celery():
    """Create the celery extension."""
    backend = "redis://redis:6379"
    broker = "redis://redis:6379"
    celery = Celery(__name__, backend=backend, broker=broker)
    # celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    # celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    return celery


def init_celery(celery, app):
    """Initialize the celery extension."""
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


celery = make_celery()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Image Processing system.",
        "description": "An application for managing image resizing and upload to AWS S3.",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "lyceokoth@gmail.com",
            "url": "www.twitter.com/lylethedesigner",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0"
    },
    "host": LazyString(lambda: request.host),
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example:\"Authorization: Bearer {token}\""
        }
    },
}


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(template=swagger_template,
                  config=swagger_config)