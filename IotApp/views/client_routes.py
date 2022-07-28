from datetime import datetime
from .. import models
from .. import schemas
from sqlalchemy.exc import DBAPIError
from flask import render_template, url_for, redirect, request, abort
from . import cors, cross_origin, app




@app.route('/')
def index():
    return redirect(url_for('documentation'))

@app.route("/docs")
def documentation():
    print("hello")
    return render_template("docs.html")

@app.route("/control/rgb/")
def rgbUI():
    print("hello")
    return render_template("home.html")

# For getting all enrolled devices
@app.route('/fetchall/device/')
def getdevicedata(db=models.Session()):
    data = db.query(models.Device).all()
    db.close()
    data = [i._tojson() for i in data]
    res = {}
    res['data'] = data
    return res, 200


# For getting the device info by device id
@app.route("/fetch/device/")
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

# For fetching data from dht
@app.route("/fetch/dht/")
@cross_origin()
def fetch_dht(
        db = models.Session()
):
    device_id = int(request.args.get('device_id'))

    db_dht_data = db.query(models.DHT).filter(models.Device.id==device_id).order_by(models.DHT.last_update.desc()).all()
    if db_dht_data ==[]:
        db.close()
        return {'message':'no data found'}, 404

    db_dht_data = [obj._tojson() for obj in db_dht_data]
    db.close()
    response = {}

    response['data'] = db_dht_data
    return response, 200

@app.route('/update/rgb/',methods=['POST'])
@cross_origin()
def update_rgb(
    db=models.Session()
): 
    payload = request.json
    #db_rgb = db.query(models.RGB).filter(models.RGB.device_id==payload['device_id']).first()
    
    #if db_rgb is None:
    new_rgb = models.RGB(
                            device_id = payload['device_id'],
                            red = payload['red'],
                            green = payload['green'],
                            blue = payload['blue'],
                            is_on = payload['on'],
                            last_update = datetime.now()
                        )
    db.add(new_rgb)
    db.commit()
    db.refresh(new_rgb)
    db.close()
    res={}
    res['data'] = new_rgb._tojson()
    return res,201
    
    '''else:
        db_rgb.red = payload['red']
        db_rgb.green = payload['green']
        db_rgb.blue = payload['blue']
        db_rgb.is_on = payload['on']
        db_rgb.last_update = datetime.now()
        
        
        db.commit()
        db.refresh(db_rgb)
        db.close()
    
        res={}
        res['data'] = db_rgb._tojson()
        return res,201'''
    
    
    
