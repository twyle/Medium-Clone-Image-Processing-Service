from flask import jsonify, current_app
from werkzeug.utils import secure_filename
from os import path
from ..extensions.extensions import s3


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
            return jsonify({'error': str(e)}), 400
        else:
            data = "{}{}".format(current_app.config["S3_LOCATION"], path.basename(file.name))
            return jsonify({'File succesfully uploaded': data}), 200


def allowed_file(filename: str) -> bool:
    """Check if the file is allowed."""
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

 
def handle_upload_image(file):
    """Handle image upload."""
    if file.filename == '':
        return jsonify({'error': 'No file was chosen!'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        file_path = path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        return upload_file_to_s3(file_path, current_app.config["S3_BUCKET"])
    
    return jsonify({'error': 'The file type is not allowed!'}), 400
    