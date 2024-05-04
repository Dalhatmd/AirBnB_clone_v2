#!/usr/bin/python3
""" Implementation of Database storage engine"""
import os
from models.base_model import Base
from sqlalchemy import create_engine, sessionmaker, scoped_session


usr = os.getenv('HBNB_MYSQL_USER')
paswd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
database = os.getenv('HBNB_MYSQL_DB')

connection = f"mysql+pymysql://{usr}:{paswd}@{host}/{database}"
class DBStorage:
    """ Database Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """initialiser"""
        self.__engine = create_engine(connection, pool_pre_ping=True)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """lists all items in current session """
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = namedclass.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in namedclass.values:
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects
            

    def new(self, obj):
        """ adds an object """
        self.__session.commit()

    def save(self):
        """ saves the current session """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes an object """
        if obj is None:
            continue
        else:
            self.__session.delete(obj)

    def reload(self):
        """ reloads objects from database """
        factory = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(factory)

    def close(self):
        """ close current session """
        self.__session.remove()

    def get(self, cls, id):
        """ gets an object """
        if cls and type(cls) == str and id and type(id)\
        is str and cls in namedclass:
            cls = namedclass[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls, id):
        """ counts the number of objects """
        total = 0
        if type(cls) == str and cls in namedclass:
            cls = namedclass[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in namedclass.values:
                total += self.__session.query(cls).count()
        return total
