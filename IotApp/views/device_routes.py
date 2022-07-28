from datetime import datetime
from .. import models
from .. import schemas
from sqlalchemy.exc import DBAPIError
from flask import render_template, url_for, redirect, request, abort
from . import cors, cross_origin, app


# For getting is_exist from device
@app.route("/node/status/")
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

# For enrolling a new device, this method is meant to be called from a device
@app.route("/node/enrolldevice/", methods = ["POST"])
@cross_origin()
def enroll_device(
                  db=models.Session()
                  ):
    try:
        
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

    except Exception as e:
        err = str(e)
        abort(406, err)

# This will create dht11 table from post method and receiving data from device.
@app.route("/node/update/dht/", methods = ['POST'])
@cross_origin()
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


# This route for get the data for RGB table
@app.route('/node/fetch/rgb/')
def fetch_rgb(
    db=models.Session()
):
    chip_id = str(request.args.get('chip_id'))

    db_device_id = db.query(models.Device).filter(models.Device.chip_id == chip_id).first()
    db_device_id = db_device_id.id
    
    db_rgb = db.query(models.RGB).filter(models.RGB.device_id == db_device_id).order_by(models.RGB.last_update.desc()).first()
    print(db_rgb)
    res={}
    if db_rgb.is_on == 0:
        db.close()
        return {'red':0,'green':0,'blue':0}, 200
    db.close()
    res['red'] = db_rgb.red
    res['green'] = db_rgb.green
    res['blue'] = db_rgb.blue

    return res,200
    
    

