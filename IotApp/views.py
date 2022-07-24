from datetime import datetime
from IotApp import app
from . import models
from . import schemas
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session
from flask_pydantic import validate
from flask import render_template, url_for, redirect, request, abort


@app.route('/')
def index():
    return redirect(url_for('documentation'))


@app.route("/docs")
def documentation():
    print("hello")
    return render_template("docs.html")

# For enrolling a new device, this method is meant to be called from a device
@app.route("/enrolldevice/", methods = ["POST"])
def enroll_device(
                  db=models.Session()
                  ):
    try:
        
        data = request.get_json()
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
        return {"status":"bad request"}, 406

