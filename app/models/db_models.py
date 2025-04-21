# app/models/db_models.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Bunches(Base):
    __tablename__ = "bunches"
    id               = Column(Integer, primary_key=True, index=True)
    upload_id        = Column(Integer, nullable=False)
    latitude         = Column(Float, nullable=True)
    longitude        = Column(Float, nullable=True)
    # backref from Berries
    berries          = relationship("Berries", back_populates="bunch")

class Berries(Base):
    __tablename__ = "berries"
    id               = Column(Integer, primary_key=True, index=True)
    bunch_id         = Column(Integer, ForeignKey("bunches.id"), nullable=False)
    axis_1           = Column(Float, nullable=True)
    axis_2           = Column(Float, nullable=True)
    axis_3           = Column(Float, nullable=True)
    bunch            = relationship("Bunches", back_populates="berries")

