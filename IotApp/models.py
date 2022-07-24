from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
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



class Device(Base,JsonModel):
    
    __tablename__ = 'device'
    
    id = Column(Integer, primary_key = True)
    chip_id = Column(String(100), nullable = False)
    location = Column(String(100))
    description = Column(String(1000))
    is_active = Column(Integer)
    enrolled_at = Column(Date)




    