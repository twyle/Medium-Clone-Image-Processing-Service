import os
from ..auth.models import User
from ..extensions.extensions import db
import re
from flask import current_app
from ..exceptions import UserNameTooLong, UserNameTooShort


def create_db_():
    """Create the database and all the tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()


def is_user_name_valid(user_name: str) -> bool:
    """Check if the user name is valid."""
    if not user_name:
        raise ValueError("The user_name has to be provided.")

    if not isinstance(user_name, str):
        raise ValueError("The user_name has to be string")

    if len(user_name) >= current_app.config["NAME_MAX_LENGTH"]:
        raise UserNameTooLong(
            f'The user_name has to be less than {current_app.config["NAME_MAX_LENGTH"]}'
        )

    if len(user_name) <= current_app.config["NAME_MIN_LENGTH"]:
        raise UserNameTooShort(
            f'The user_name has to be more than {current_app.config["NAME_MIN_LENGTH"]}'
        )

    return True


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError("The email_address cannot be an empty value")

    if not isinstance(email_address, str):
        raise ValueError("The email_address must be a string")

    #  Regular expression for validating an Email
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(regex, email_address):
        return True

    return False
    

def check_if_user_with_id_exists(user_id: int) -> bool:
    """Check if the user with the given user_id exists."""
    if not user_id:
        raise ValueError("The user_id has to be provided.")

    if not isinstance(user_id, int):
        raise ValueError("The user_id has to be an integer")

    user = User.query.filter_by(id=user_id).first()

    if user:
        return True

    return False


def check_if_email_id_match(email: str, id: int) -> bool:
    """Check if user id and email belong to same user."""
    if not id:
        raise ValueError("The user id has to be provided!")

    if not isinstance(id, int):
        raise ValueError("The id has to be an int")

    if not email:
        raise ValueError("The email has to be provided.")

    if not isinstance(email, str):
        raise ValueError("The user_email has to be an string")

    user = User.query.filter_by(id=id).first()

    if user.email == email:
        return True

    return False


def check_if_user_exists(user_email: str) -> bool:
    """Check if the admin with the given user_email exists."""
    if not user_email:
        raise ValueError('The user_email has to be provided.')

    if not isinstance(user_email, str):
        raise ValueError('The user_email has to be an integer')

    user = User.query.filter_by(email=user_email).first()

    if user:
        return True

    return False


def set_flask_environment(app) -> str:
    """Set the flask development environment.
    Parameters
    ----------
    app: flask.Flask
        The flask application object
    Raises
    ------
    KeyError
        If the FLASK_ENV environment variable is not set.
    Returns
    -------
    str:
        Flask operating environment i.e development
    """
    try:
        if os.environ['FLASK_ENV'] == 'production':  # pragma: no cover
            app.config.from_object('api.config.config.ProductionConfig')
        elif os.environ['FLASK_ENV'] == 'development':  # pragma: no cover
            app.config.from_object('api.config.config.DevelopmentConfig')
        elif os.environ['FLASK_ENV'] == 'test':
            app.config.from_object('api.config.config.TestingConfig')
        elif os.environ['FLASK_ENV'] == 'stage':
            app.config.from_object('api.config.config.StagingConfig')
    except KeyError:
        app.config.from_object('api.config.config.DevelopmentConfig')
        return 'development'

    return os.environ['FLASK_ENV']