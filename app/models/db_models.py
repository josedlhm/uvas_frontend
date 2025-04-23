# app/models/db_models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

class Upload(Base):
    __tablename__ = "uploads"
    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    upload_timestamp = Column(String, nullable=False)
    created_at       = Column(DateTime, default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "upload_timestamp", name="uix_user_upload"),
    )

    bunches = relationship(
        "Bunches",
        back_populates="upload",
        cascade="all, delete-orphan"
    )

class Bunches(Base):
    __tablename__ = "bunches"
    id                    = Column(Integer, primary_key=True, index=True)
    user_id               = Column(Integer, ForeignKey("users.id"), nullable=False)
    upload_id             = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    latitude              = Column(String, nullable=True)
    longitude             = Column(String, nullable=True)
    created_at            = Column(DateTime, default=func.now())
    n_visible_berries     = Column(Integer, nullable=True)  # new
    n_estimated_berries   = Column(Integer, nullable=True)  # new

    upload = relationship("Upload", back_populates="bunches")
    berries = relationship(
        "Berries",
        back_populates="bunch",
        cascade="all, delete-orphan"
    )

class Berries(Base):
    __tablename__ = "berries"
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    upload_id   = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    axis_1      = Column(Float, nullable=True)
    axis_2      = Column(Float, nullable=True)
    axis_3      = Column(Float, nullable=True)
    berry_size  = Column(Float, nullable=True)               # new
    bunch_id    = Column(Integer, ForeignKey("bunches.id"), nullable=False)
    created_at  = Column(DateTime, default=func.now())

    bunch = relationship("Bunches", back_populates="berries")
