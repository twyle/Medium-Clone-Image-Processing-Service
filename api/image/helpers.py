from flask import jsonify, current_app
from werkzeug.utils import secure_filename
from os import path


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
        
        return jsonify({'success': 'The image was uploaded'}), 200
    
    return jsonify({'error': 'The file type is not allowed!'}), 400
    