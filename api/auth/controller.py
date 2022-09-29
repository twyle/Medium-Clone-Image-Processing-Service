# -*- coding: utf-8 -*-
"""This module has methods that are used in the other modules in this package."""
from flask import current_app, jsonify

from ..exceptions import (
    EmailAddressTooLong,
    EmptyUserData,
    InvalidEmailAddressFormat,
    MissingEmailData,
    MissingEmailKey,
    MissingNameData,
    MissingNameKey,
    NonDictionaryUserData,
    UserExists,
    UserNameTooLong,
    UserNameTooShort,
)
from ..extensions.extensions import db
from ..helpers.helpers import check_if_user_exists, is_email_address_format_valid
from .helpers import is_user_name_valid, handle_upload_image
from .models import User, user_schema


def create_new_user(user_data: dict, profile_pic) -> dict:
    """Create a new user."""
    if not user_data:
        raise EmptyUserData("The user data cannot be empty.")

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData("user_data must be a dict")

    if "Email" not in user_data.keys():
        raise MissingEmailKey("The email is missing from the user data")

    if not user_data["Email"]:
        raise MissingEmailData("The email data is missing")

    if len(user_data["Email"]) >= current_app.config["EMAIL_MAX_LENGTH"]:
        raise EmailAddressTooLong(
            f'The email address should be less than {current_app.config["EMAIL_MAX_LENGTH"]} characters!'
        )

    if not is_email_address_format_valid(user_data["Email"]):
        raise InvalidEmailAddressFormat("The email address is invalid")

    is_user_name_valid(user_data["User Name"])


    if check_if_user_exists(user_data["Email"]):
        raise UserExists(f'The email adress {user_data["Email"]} is already in use.')
            
    user = User(
        email=user_data["Email"],
        name=user_data["User Name"]
    )
    
    if profile_pic:
        if profile_pic["Profile Picture"]:
            profile_pic = handle_upload_image(profile_pic["Profile Picture"])
            user.profile_pic = profile_pic

    db.session.add(user)
    db.session.commit()

    return user_schema.dumps(user)


def handle_create_user(user_data: dict, profile_pic):
    """Handle the POST request to the /api/v1/user route."""
    try:
        registered_user_data = create_new_user(user_data, profile_pic)
    except (
        EmptyUserData,
        NonDictionaryUserData,
        MissingEmailKey,
        MissingNameKey,
        EmailAddressTooLong,
        InvalidEmailAddressFormat,
        UserExists,
        MissingEmailData,
        MissingNameData,
        UserNameTooShort,
        UserNameTooLong,
    ) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return registered_user_data, 201