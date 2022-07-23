
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///openiot.db', echo=True)
Base = declarative_base()


# Model Table Classes



class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key = True)
    ip = Column(String)
    location = Column(String)
    description = Column(String)
    is_active = Column(Integer)
    enrolled_at = Column(Date)

    def __init__(self,id,ip,location,description,is_active,enrolled_at):
        self.id = id
        self.ip = ip
        self.location = location
        self.description = description
        self.is_active = is_active
        self.enrolled_at = enrolled_at






if __name__=="__main__":
    Base.metadata.create_all(engine)