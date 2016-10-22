from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from backend.utils.pluralize import pluralize


Base = declarative_base()


class Defaults:

    @declared_attr
    def __tablename__(cls):
        return pluralize(cls.__name__.lower())


class BaseDefaults(Defaults):

    id = Column(Integer, primary_key=True)

    def as_dict(self):
        return {"id": self.id}


class Contact(BaseDefaults, Base):

    name = Column(String(256))

    def as_dict(self):
        data = super(Contact, self).as_dict()

        if self.name:
            data["name"] = self.name

        return data
