#!/usr/bin/python3
"""BaseModel Module"""
from datetime import datetime
import uuid
import models


class BaseModel:
    """
    Class BaseModel that defines all common
    attributes/methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """Initializates a new instance of BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Return a informal string about a BaseModel instance:
        [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """
        Updates the public instance attribute
        updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values
        of __dict__ of the instance
        """
        i_dict = self.__dict__.copy()
        i_dict["__class__"] = self.__class__.__name__
        if hasattr(self, "created_at"):
            i_dict["created_at"] = self.created_at.isoformat()
        if hasattr(self, "updated_at"):
            i_dict["updated_at"] = self.updated_at.isoformat()
        return i_dict
