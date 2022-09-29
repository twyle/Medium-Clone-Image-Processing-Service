from flask import current_app
from ..exceptions import UserNameTooLong, UserNameTooShort, EmptyImageFile, IllegalFileType
from PIL import Image
import json
from werkzeug.utils import secure_filename
import numpy as np
from ..tasks import upload_file_to_s3


def allowed_file(filename: str) -> bool:
    """Check if the file is allowed."""
    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def upload_image(file):
    """Upload image to S3."""
    if not file:
        raise EmptyImageFile("The file has to be provided!")
    if file.filename == "":
        raise EmptyImageFile("The file has to be provided!")
    if not allowed_file(file.filename):
        raise IllegalFileType("That file type is not allowed!")

    img = Image.open(file)
    json_data = json.dumps(np.array(img).tolist())
    filename = secure_filename(file.filename)

    upload_file_to_s3.delay(json_data, filename, current_app.config["S3_BUCKET"])

    profile_pic = f"{current_app.config['S3_LOCATION']}{filename}"

    return profile_pic


def handle_upload_image(file):
    """Handle image upload."""
    try:
        profile_pic = upload_image(file)
    except (EmptyImageFile, IllegalFileType, ValueError, TypeError) as e:
        raise e
    except Exception as e:
        raise e
    else:
        return profile_pic


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
