from IotApp import app, models
import os


if __name__=="__main__":
    
    if not os.path.exists("openiot.db"):
        models.Base.metadata.create_all(models.engine)
    
    # not for production
    app.run(host="192.168.18.229",debug=True)