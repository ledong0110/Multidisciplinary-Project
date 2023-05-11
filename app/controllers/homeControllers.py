from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, session, render_template, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import ast
import os
from app.model.IOTDevice import IOTDevice
from app.model.RoadData import RoadData
from sqlalchemy import and_
from config.database.db import db
import base64

api = Namespace('home', description='home page')

# upload_parser = api.parser()
# upload_parser.add_argument('file', location='files',
#                            type=FileStorage, required=True)

# ALLOWED_EXTENSIONS = ['json']

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# upload_parser = api.parser()
# upload_parser.add_argument('device_id', type=str, location='form')
# upload_parser.add_argument('temp', type=float, location='form')
# upload_parser.add_argument('hummid', type=float, location='form')
# upload_parser.add_argument('rain', type=int, location='form')

upload_parser = api.model('upload_form', {
    'device_id': fields.String(default='iot_1'),
    'temp': fields.Float(default=31),
    'hummid': fields.Float(default=52),
    'rain': fields.Integer(default=0)
})

# image_parser = api.parser()
# image_parser.add_argument('image', type=str, location='form')
# image_parser.add_argument('flood_level', type=int, location='form')
image_parser = api.model('image_form', {
    'device_id': fields.String(default='iot_1'),
    'image': fields.String(default='test1'),
    'flood_level': fields.Integer(default=1),
})

device_parser = api.model('device_form', {
    'device_ids': fields.String(default="['iot_1']"),
})

# devices_parser = api.parser()
# devices_parser.add_argument('device_ids', type=list, location='form')
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
    def get(self):
        args = request.args.to_dict()
        data = None
        if "id" in args and args["id"]:
            data = db.session.query(RoadData).filter(RoadData.id == id).first().to_dict()
        elif "device_id" in args and "latest" in args and args["device_id"] and args["latest"]:
            data = db.session.query(RoadData).filter(RoadData.device_id == args["device_id"]).order_by(RoadData.id.desc()).first().to_dict()
        else:
            data = db.session.query(RoadData).filter(RoadData.device_id == args["device_id"]).all()
            data = list(map(lambda x: x.to_dict(), data))
        return jsonify(data)

@api.route('/getImage')
class Data(Resource):
    @api.expect(dataForm)
    def get(self):
        args = request.args.to_dict()
        data = None
        if "id" in args and args["id"]:
            data = db.session.query(RoadData).filter(RoadData.id == args["id"]).first()
        elif "device_id" in args and "latest" in args and args["device_id"] and args["latest"]:
            data = db.session.query(RoadData).filter(and_(RoadData.device_id == args["device_id"], RoadData.image.isnot(None))).order_by(RoadData.id.desc()).first()
        else:
            return jsonify({"msg": "Error"}), 500
        if not data:
            return jsonify({"msg": "There is no data in database"})
        image_name = str(data.image)
        with open(f'{os.environ.get("STORAGE")}/image/{image_name}.jpg', "rb") as f:
            img = f.read()
            encodeImage = base64.b64encode(img).decode()
        return jsonify({"image": encodeImage})

@api.route('/getDeviceInfo')
class DeviceInfo(Resource):
    @api.expect(deviceForm)
    def get(self):
        args = request.args.to_dict()
        data = None
        if "id" in args and args["id"]:
            data = db.session.query(IOTDevice).filter(IOTDevice.id == id).first().to_dict()
        elif "device_id" in args and args["device_id"]:
            data = db.session.query(IOTDevice).filter(IOTDevice.device_id == device_id).first().to_dict()
        elif "address" in args and args["address"]:
            data = db.session.query(IOTDevice).filter(IOTDevice.address == address).first().to_dict()
        else:
            data = db.session.query(IOTDevice).all()
            data = list(map(lambda x: x.to_dict(), data))
        return jsonify(data)
    
@api.route('/storeData')
class StoreData(Resource):
    @api.expect(upload_parser, validate=False)
    def post(self):
        args = request.get_json()
        roadData = RoadData(device_id=args["device_id"], temp=args["temp"], hummid=args["hummid"], rain=1-int(args["rain"]))
        db.session.add(roadData)
        db.session.commit()
        return {"msg": "done"}

@api.route('/storeImageName')
class StoreImageName(Resource):
    @api.expect(image_parser, validate=False)
    def post(self):
        args = request.get_json()
        roadData = db.session.query(RoadData).filter(RoadData.device_id == args['device_id']).order_by(RoadData.id.desc()).first()
        roadData.image = args['image']
        roadData.flood_level = int(args['flood_level'])
        db.session.commit()
        return {"msg": "done"}

@api.route('/updateActiveDevice')
class UpdateActiveDevice(Resource):
    @api.expect(device_parser, validate=False)
    def post(self):
        args = request.get_json()
        list_device = ast.literal_eval(args['device_ids'])
        db.session.query(IOTDevice).filter(IOTDevice.device_id.in_(list_device)).update({"state": 1}, synchronize_session = False)
        db.session.query(IOTDevice).filter(IOTDevice.device_id.not_in(list_device)).update({"state": 0}, synchronize_session = False)
        db.session.commit()
        return {"msg": "done"}
    
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
