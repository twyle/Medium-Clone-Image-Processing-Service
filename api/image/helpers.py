from flask import jsonify, current_app
from werkzeug.utils import secure_filename
from os import path
import re
from ..extensions.extensions import s3, db
from .models import User
from .exceptions import (
    EmptyImageFile,
    IllegalFileType,
    UserDoesNotExist,
    InvalidEmailAddressFormat
)


def update_profile_pic(profile_pic_path: str, email: str):
    """Saves the profile pic path in database"""
    pass    


def upload_file_to_s3(file_path, bucket_name):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    with open(file_path, 'rb') as file:
        try:
            s3.upload_fileobj(
                file,
                bucket_name,
                path.basename(file.name)
            )
        except Exception as e: 
            raise e
        else:
            data = "{}{}".format(current_app.config["S3_LOCATION"], path.basename(file.name))
            return data


def allowed_file(filename: str) -> bool:
    """Check if the file is allowed."""
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    print(filename.rsplit('.', 1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file):
    """Saves the file locally"""
    filename = secure_filename(file.filename)    
    file.save(path.join(current_app.config['UPLOAD_FOLDER'], filename))
    file_path = path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    return file_path

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


def is_email_address_format_valid(email_address: str) -> bool:
    """Check that the email address format is valid."""
    if not email_address:
        raise ValueError('The email_address cannot be an empty value')

    if not isinstance(email_address, str):
        raise ValueError('The email_address must be a string')

    #  Regular expression for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(regex, email_address):
        return True

    return False

def upload_image(file, email):
    """Uploads image to S3"""
    if not email:
        raise ValueError('The email has to e provided')
    if not isinstance(email, str):
        raise TypeError('The email has to be a string')
    if not is_email_address_format_valid(email):
        raise InvalidEmailAddressFormat('Invalid email address format')
    if not check_if_user_exists(email):
        raise UserDoesNotExist(f'There is no user with email {email}')
    if not file:
        raise EmptyImageFile('The file has to be provided!')
    if file.filename == '':
        raise EmptyImageFile('The file has to be provided!')
    if not allowed_file(file.filename):
        raise IllegalFileType('That file type is not allowed!')
    
    file_path = save_file(file)
    
    profile_pic = upload_file_to_s3(file_path, current_app.config["S3_BUCKET"])
    
    return profile_pic

def update_user(email: str, profile_pic: str):
    """Sets the users profile pic info."""
    user = User.query.filter_by(email=email).first()
    if user:
        user.profile_pic = profile_pic
        db.session.commit()
        print('updated profile pic')

 
def handle_upload_image(file, email):
    """Handle image upload."""
    try:
        profile_pic = upload_image(file, email)
        print(profile_pic)
    except (
        EmptyImageFile,
        IllegalFileType,
        ValueError,
        TypeError,
        UserDoesNotExist,
        InvalidEmailAddressFormat
    ) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    else:
        update_user(email, profile_pic)
        return jsonify({'Success': f'Profile pic for {email} set.'}), 200