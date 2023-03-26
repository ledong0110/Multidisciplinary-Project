from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, session, render_template, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from app.model.User import User
from config.database.db import db

api = Namespace('home', description='home page')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

ALLOWED_EXTENSIONS = ['json']

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/register/<string:username>')
class Home(Resource):
    @api.expect(upload_parser, validate=True)
    def post(self, username: str):
        args = upload_parser.parse_args()
        file = args['file']
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.environ.get('STORAGE'), f"{username}.json"))
            db.session.add(User(username=username))
            db.session.commit()
            resp = jsonify({'message' : 'successfully register'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp