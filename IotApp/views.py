from datetime import datetime
from IotApp import app
from . import models
from . import schemas
from sqlalchemy.exc import DBAPIError
from flask import render_template, url_for, redirect, request, abort
from flask_cors import CORS, cross_origin

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/fetchdevice/')
def getdevicedata(db=models.Session()):
    data = db.query(models.Device).all()
    db.close()
    data = [i._tojson() for i in data]
    res = {}
    res['data'] = data
    return res, 200


@app.route('/')
def index():
    return redirect(url_for('documentation'))

@app.route("/docs")
def documentation():
    print("hello")
    return render_template("docs.html")

# For enrolling a new device, this method is meant to be called from a device
@app.route("/enrolldevice/", methods = ["POST"])
@cross_origin()
def enroll_device(
                  db=models.Session()
                  ):
    #try:
        
    data = request.json
    print(data)
    chip_id = data["chip_id"]
    db_device = db.query(models.Device).filter(models.Device.chip_id == chip_id).first()
    if db_device is None:
        
        new_device = models.Device(
                                chip_id = chip_id,
                                location = data["location"],
                                description = data["description"],
                                enrolled_at = datetime.now(),
                                is_active = 1
                            )
        
        db.add(new_device)
        try:
            db.commit()
            db.refresh(new_device)
        except DBAPIError:
            db.rollback()
            abort(400, "bad request")
        
        db.close()
    else:
        db.close()
        return {"status":"already exist", "id":db_device.id},208

    response = {} 
    
    response['data'] = new_device._tojson()
    return response,201

    '''except Exception as e:
        err = str(e)
        abort(406, err)'''

# For getting the device info by device id
@app.route("/device/")
def device_info(
    db = models.Session()
):
    try:
        device_id = request.args.get('id')
        db_device = db.query(models.Device).get(device_id)
        db.close()
        if db_device is None:

            return {"message":"resource not found"}, 404
        db_device = db_device._tojson()

        return {"status":"ok", "device_data":db_device}

    except Exception as e:
        err = str(e)
        print(err)
        return {"status":"bad request"}, 406

# For getting is_exist from device
@app.route("/devicestatus/")
@cross_origin()
def device_status(
    db = models.Session()
):
    try:
        chip_id = request.args.get("chip_id")
        db_device = db.query(models.Device).filter(models.Device.chip_id == chip_id).first()
        db.close()
        if db_device is None:
            return {"status":"not found"}, 404
        else:
            return {"id":db_device.id}, 200

    except Exception as e:
        err = str(e)
        print(err)
        return {"status":"bad request"}, 400

# This will create dht11 table from post method and receiving data from device.
@app.route("/update/dht/", methods = ['POST'])
def update_dht(
    db = models.Session()
):
    payload_data = request.get_json()
    db_device_id = db.query(models.Device).filter(models.Device.chip_id ==payload_data['chip_id']).first()
   
    if db_device_id is None:
        db.close()
        return {'message':'data is not found'},404

    #db_device_id = db_device_id.id
    new_temp = payload_data['temperature']
    new_humid = payload_data['humidity']
    curr_update = datetime.now()

    new_dht_data = models.DHT(device_id = db_device_id.id,
                                temperature =new_temp,
                                humidity = new_humid,
                                last_update = curr_update)
    
    db.add(new_dht_data)
    db.commit()
    db.refresh(new_dht_data)
    db.close()

    return {'message':'new resource has been created'},201


# this is creating for fetching data from dht11 from get method
@app.route("/fetch/dht/")
def fetch_dht(
        db = models.Session()
):


    db_dht_data = db.query(models.DHT).order_by(models.DHT.last_update).all()
    if db_dht_data ==[]:
        db.close()
        return {'message':'no data found'}, 404

    db_dht_data = [obj._tojson() for obj in db_dht_data]
    db.close()
    response = {}

    response['data'] = db_dht_data
    return response, 200
    
        
    
