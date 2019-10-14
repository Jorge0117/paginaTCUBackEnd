import io
import os

from flask import Blueprint, jsonify, request, make_response, send_file
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from pathlib import Path


bp_files = Blueprint('bp_files', __name__)

@bp_files.route('/upload/document', methods=['POST'])
@jwt_required
def uploadDocument():
    folder = 'documents/' + request.args.get('folder')
    allowed_files = ['.pdf']
    return uploadFile(allowed_files, folder)

@bp_files.route('/upload/image', methods=['POST'])
@jwt_required
def uploadImage():
    folder = 'images/' + request.args.get('folder')
    allowed_files = ['.png', '.jpg']
    return uploadFile(allowed_files, folder)


def uploadFile(allowed_files, folder):
    if 'archivo' not in request.files:
        return 'No se encontró el archivo', 404

    file = request.files['archivo']
    if file.filename == '':
        return 'No se encontró el archivo', 404

    filename, file_extension = os.path.splitext(file.filename)

    if file and file_extension in allowed_files:
        filename = secure_filename(file.filename)
        path = Path().cwd() / 'files' / folder

        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(path, filename)
        file.save(path)

        response = {'status': 'succeess', 'url': path}

        return jsonify(response), 200
    else:
        return 'Tipo de archivo no permitido', 400


@bp_files.route('/download', methods=['GET'])
def downloadFile():
    location = request.args.get('url')
    location = Path().cwd() / location
    filename = os.path.basename(location)
    file = open(location, 'rb')

    return send_file(
        file,
        mimetype='blob',
        as_attachment=True,
        attachment_filename=filename)

