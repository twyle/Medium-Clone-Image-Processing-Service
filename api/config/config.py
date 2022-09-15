# -*- coding: utf-8 -*-
"""This module contain the confuguration for the application."""
import os
from dotenv import load_dotenv 

load_dotenv()


class BaseConfig():
    """Base configuration."""

    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploaded-images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    S3_BUCKET = os.environ['S3_BUCKET']
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_ACCESS_SECRET = os.environ['AWS_ACCESS_SECRET']
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

    db_conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = db_conn_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Configuration used during development."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = True
    TESTING = False
    

class TestingConfig(BaseConfig):
    """Configuration used during testing."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = True
    TESTING = True
    

class StagingConfig(BaseConfig):
    """Configuration used during staging."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = False
    TESTING = False


class ProductionConfig(BaseConfig):
    """Configuration used during production."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = False
    TESTING = False