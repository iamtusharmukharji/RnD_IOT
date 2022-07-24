from IotApp import app, models
import os


if __name__=="__main__":
    
    if not os.path.exists("openiot.db"):
        models.Base.metadata.create_all(models.engine)
    
    # not for production
    app.run(debug=True)