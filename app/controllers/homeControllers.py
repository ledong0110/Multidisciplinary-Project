from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, session, render_template, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from app.model.IOTDevice import IOTDevice
from app.model.RoadData import RoadData
from config.database.db import db

api = Namespace('home', description='home page')

# upload_parser = api.parser()
# upload_parser.add_argument('file', location='files',
#                            type=FileStorage, required=True)

# ALLOWED_EXTENSIONS = ['json']

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
dataForm= api.model('dataForm', {
    'id': fields.Integer(),
    'device_id': fields.String(),
    'latest': fields.Integer(enum=[0,1])
})

deviceForm= api.model('deviceForm', {
    'id': fields.Integer(),
    'device_id': fields.String(),
    'address': fields.String()
})

@api.route('/getDatas')
class Data(Resource):
    @api.expect(dataForm)
    def get(self, id:int):
        args = request.args.to_dict()
        data = None
        if args["id"]:
            data = db.session.query(RoadData).filter(RoadData.id == id).first()
        elif args["device_id"] and args["latest"]:
            data = db.session.query(RoadData).filter(RoadData.device_id == device_id).order_by(RoadData.id.desc()).first()
        else:
            data = db.session.query(RoadData).filter(RoadData.device_id == device_id).all()
        return jsonify(data.to_dict())



@api.route('/getDeviceInfo')
class DeviceInfo(Resource):
    def get(self, id:int):
        args = request.args.to_dict()
        data = None
        if args["id"]:
            data = db.session.query(IOTDevice).filter(IOTDevice.id == id).first()
        elif args["device_id"]:
            data = db.session.query(IOTDevice).filter(IOTDevice.device_id == device_id).first()
        elif args["address"]:
            data = db.session.query(IOTDevice).filter(IOTDevice.address == address).first()
        else:
            data = db.session.query(IOTDevice).all()
        return jsonify(data.to_dict())
    

  
    
    
    # @api.expect(upload_parser, validate=True)
    # def post(self, username: str):
    #     args = upload_parser.parse_args()
    #     file = args['file']
    #     if file.filename == '':
    #         resp = jsonify({'message' : 'No file selected for uploading'})
    #         resp.status_code = 400
    #         return resp
        
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(os.environ.get('STORAGE'), f"{username}.json"))
    #         db.session.add(User(username=username))
    #         db.session.commit()
    #         resp = jsonify({'message' : 'successfully register'})
    #         resp.status_code = 201
    #         return resp
    #     else:
    #         resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
    #         resp.status_code = 400
    #         return resp