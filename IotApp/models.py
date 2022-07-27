
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///openiot.db', echo=True)
Base = declarative_base()

# for creating a session

Session = sessionmaker(bind=engine, autoflush=True)


# Model Table Classes

class JsonModel(object):
    def _tojson(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

#-------Database Schemas------------#

class Device(Base,JsonModel):
    
    __tablename__ = 'device'
    
    id = Column(Integer, primary_key = True)
    chip_id = Column(String(100), nullable = False)
    location = Column(String(100))
    description = Column(String(1000))
    is_active = Column(Integer)
    enrolled_at = Column(Date)

    def __init__(self, chip_id, location, description, is_active, enrolled_at):

        self.chip_id = chip_id
        self.location = location
        self.description = description
        self.is_active = is_active
        self.enrolled_at = enrolled_at

class DHT(Base,JsonModel):

    __tablename__ = 'dht'

    id = Column(Integer,primary_key = True)
    device_id = Column(Integer)
    temperature = Column(Integer)
    humidity = Column(Integer)
    last_update = Column(DateTime)

    def __init__(self, device_id, temperature, humidity, last_update):
    
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.last_update = last_update
    
class RGB(Base,JsonModel):
    __tablename__ = "rgb"

    id = Column(Integer,primary_key=True)
    device_id = Column(Integer)
    red = Column(Integer)
    green = Column(Integer)
    blue = Column(Integer)
    is_on = Column(Integer)    # 0 or 1
    last_update = Column(DateTime)

class Servo(Base,JsonModel):
    __tablename__ = 'servo'

    id = Column(Integer,primary_key=True)
    device_id = Column(Integer)
    angle = Column(Integer)
    last_update = Column(DateTime)

class DeviceAllocation(Base,JsonModel):
    __tablename__ = 'device_allocation'

    id = Column(Integer,primary_key=True)
    device_id = Column(Integer)
    user_id = Column(Integer)
    allocated_at = Column(DateTime)
    is_allocated = Column(Integer)  # 0 or 1

class User(Base,JsonModel):

    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(VARCHAR(1024))
    address = Column(VARCHAR(1024))
    cover_img = Column(VARCHAR(1024))
    registered_at = Column(DateTime)
    is_active = Column(Integer) 
    is_deleted = Column(Integer)