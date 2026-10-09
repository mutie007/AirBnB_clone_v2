#!/usr/bin/python3
"""City class module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class City(BaseModel, Base):
    """City class"""
    __tablename__ = "cities"

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place", backref="cities",
                              cascade="all, delete, delete-orphan")
