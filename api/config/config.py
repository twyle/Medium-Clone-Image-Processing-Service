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