#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from os import getenv

time_fmt = "%Y-%m-%d %H:%M:%S.%f"
if getenv('HBNB_TYPE_STORAGE') == 'db':
	Base = declarative_base()
else:
	Base = object

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, time_fmt)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, time_fmt)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key in dir(self):
            if not key.startswith('_'):
                value = getattr(self, key)
                if not callable(value):
                    dictionary[key] = value
        dictionary['__class__'] = self.__class__.__name__
        if 'created_at' in dictionary:
            dictionary['created_at'] = dictionary['created_at'].isoformat()
        if 'updated_at' in dictionary:
            dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        return dictionary


    def delete(self):
        """ Deletes an instance by calling the delete method """
        model.storage.delete(self)
