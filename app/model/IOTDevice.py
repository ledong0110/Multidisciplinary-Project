from sqlalchemy import Column, Integer, String, Float, Text
from config.database.db import db
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
class IOTDevice (db.Model):
    __tablename__ = "IOTDevice"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(127), nullable=False, unique=True) 
    state = Column(Integer)
    address = Column(String(255), nullable=False) 
    district = Column(String(255))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
