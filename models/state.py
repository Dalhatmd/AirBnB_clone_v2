#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        state = relationship('City', cascade='all, delete',
                              backref='states')

    else:
        name = ""

    @property
    def cities(self):
        """ returns the list of cities associated with this state """
        return [city for city in City.query.filter(state_id=State.id).all()]
