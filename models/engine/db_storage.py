#!/usr/bin/python3
""" Implementation of Database storage engine"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User  # Assuming you have a User model defined in models.user
from models.place import Place  # Assuming you have a Place model defined in models.place
from models.city import City  # Assuming you have a City model defined in models.city
from models.state import State  # Assuming you have a State model defined in models.state
from models.amenity import Amenity  # Assuming you have an Amenity model defined in models.amenity
from models.review import Review  # Assuming you have a Review model defined in models.review

usr = os.getenv('HBNB_MYSQL_USER')
paswd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
database = os.getenv('HBNB_MYSQL_DB')

connection = f"mysql+pymysql://{usr}:{paswd}@{host}/{database}"

namedclass = {
    "User": User,
    "Place": Place,
    "City": City,
    "State": State,
    "Amenity": Amenity,
    "Review": Review
}

class DBStorage:
    """ Database Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """initialiser"""
        self.__engine = create_engine(connection, pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        self.reload()

    def all(self, cls=None):
        """lists all items in current session """
        objects = {}
        if isinstance(cls, str):
            cls = namedclass.get(cls)
        if cls:
            query = self.__session.query(cls)
            for obj in query:
                objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        else:
            for cls in namedclass.values():
                query = self.__session.query(cls)
                for obj in query:
                    objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return objects

    def new(self, obj):
        """ adds an object """
        self.__session.add(obj)

    def save(self):
        """ saves the current session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes an object """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reloads objects from database """
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)
        Base.metadata.create_all(self.__engine)

    def close(self):
        """ close current session """
        self.__session.remove()

    def get(self, cls, id):
        """ gets an object """
        if isinstance(cls, str):
            cls = namedclass.get(cls)
        if cls:
            return self.__session.query(cls).get(id)
        return None

    def count(self, cls=None):
        """ counts the number of objects """
        total = 0
        if isinstance(cls, str):
            cls = namedclass.get(cls)
        if cls:
            total = self.__session.query(cls).count()
        else:
            for cls in namedclass.values():
                total += self.__session.query(cls).count()
        return total

