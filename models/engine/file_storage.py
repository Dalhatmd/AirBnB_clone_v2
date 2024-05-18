#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        input_obj = {}
        for key, obj in self.__objects.items():
            if isinstance(obj, cls):
                input_obj[key] = obj
        return input_obj

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects[obj.to_dict()['__class__'] + '.' + obj.id] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for key in self.__objects:
            temp[key] = self.__objects[key].to_dict(save_to_disk=True)
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in oj:
                self.__objects[key] = classes[oj[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """Deletes an object if it exists"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
