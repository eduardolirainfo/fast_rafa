import os
import uuid

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def accepted_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_file(file):
    ext = file.rsplit('.', 1)[1].lower()
    unique_file = uuid.uuid4().hex
    return f'{unique_file}.{ext}'


def save_file_locally(file):
    if file and accepted_file(file.filename):
        filename = generate_unique_file(file.filename)
        filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return {'errors': str(e)}

        return {'url': f'/{UPLOAD_FOLDER}/{filename}'}
    else:
        return {'errors': 'File type not allowed'}
