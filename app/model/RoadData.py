from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from config.database.db import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

base = declarative_base()
class RoadData (db.Model):
    __tablename__ = "RoadData"
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_date = Column(DateTime(timezone=True), default=func.now())
    device_id = Column(String(127), ForeignKey("IOTDevice.device_id"), nullable=False, unique=True) 
    temp  = Column(Float, default=0.0)
    hummid = Column(Float, default=0.0)
    rain = Column(Integer, default=0)
    flood_level = Column(Integer, default=0)
    image = Column(String(127)) 

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}