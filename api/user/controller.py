import os
from ..exceptions import (
    EmptyUserData,
    UserDoesNotExist,
    NonDictionaryUserData,
    EmailAddressTooLong,
    UserExists,
    InvalidEmailAddress,
    UserNameTooLong,
    UserNameTooShort,
    MissingEmailData,
    MissingNameData
)
from flask import jsonify, current_app
from ..helpers.helpers import (
    check_if_user_with_id_exists,
    is_email_address_format_valid,
    check_if_user_exists,
    is_user_name_valid
)
from ..extensions.extensions import db
from ..auth.models import user_schema, User
from ..auth.helpers import handle_upload_image
from ..tasks import delete_file_s3


def update_user(user_id: str, user_data: dict, profile_pic_data) -> dict:
    """Update the user with the given id."""
    if not user_id:
        raise EmptyUserData("The user_id has to be provided.")

    if not isinstance(user_id, str):
        raise ValueError("The user_id has to be a string.")

    user_id = int(user_id)

    if not check_if_user_with_id_exists(user_id):
        raise UserDoesNotExist(f"The user with id {user_id} does not exist.")

    if not user_data:
        raise EmptyUserData("The user data cannot be empty.")

    if not isinstance(user_data, dict):
        raise NonDictionaryUserData("user_data must be a dict")

    valid_keys = ["User Name", "Email"]
    for key in user_data.keys():
        if key not in valid_keys:
            raise KeyError(f"Invalid key {key}. The valid keys are {valid_keys}.")

    if "Email" in user_data.keys():
        is_email_address_format_valid(user_data["Email"])

        if len(user_data["Email"]) >= current_app.config["EMAIL_MAX_LENGTH"]:
            raise EmailAddressTooLong("The email address is too long")

        if check_if_user_exists(user_data["Email"]):
            raise UserExists(
                f'The email adress {user_data["Email"]} is already in use.'
            )

    if "User Name" in user_data.keys():
        is_user_name_valid(user_data["User Name"])

    user = User.query.filter_by(id=user_id).first()
    if "Email" in user_data.keys():
        user.email = user_data["Email"]
    if "User Name" in user_data.keys():
        user.name = user_data["User Name"]
        

    if profile_pic_data["Profile Picture"]:
        if user.profile_pic:
            delete_file_s3.delay(os.path.basename(user.profile_pic))
        profile_pic = handle_upload_image(profile_pic_data["Profile Picture"])
        user.profile_pic = profile_pic

    db.session.commit()

    return user_schema.dumps(user)


def handle_update_user(user_id: str, user_data: dict, profile_pic):
    """Handle the GET request to the /api/v1/user route."""
    try:
        user = update_user(user_id, user_data, profile_pic)
    except (
        UserExists,
        InvalidEmailAddress,
        UserNameTooShort,
        UserNameTooLong,
        EmailAddressTooLong,
        MissingNameData,
        MissingEmailData,
        NonDictionaryUserData,
        ValueError,
        EmptyUserData,
        UserDoesNotExist,
    ) as e:
        return jsonify({"error": str(e)}), 400
    else:
        return user, 200