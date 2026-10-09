#!/usr/bin/python3
"""User class module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class User(BaseModel, Base):
    """User class"""
    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
