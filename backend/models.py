import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from backend.utils.pluralize import pluralize

logger = logging.getLogger(__name__)


Base = declarative_base()


class Defaults:

    @declared_attr
    def __tablename__(cls):
        return pluralize(cls.__name__.lower())


class BaseDefaults(Defaults):

    id = Column(Integer, primary_key=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}


class Contact(BaseDefaults, Base):

    name = Column(String(256))
    nickname = Column(String(256))

    protocols = relationship("Account", back_populates="contact")


participants_table = Table(
    'conversation_participants', Base.metadata,
    Column("account_id", Integer, ForeignKey("accounts.id")),
    Column("conversation_id", Integer, ForeignKey("conversations.id")))


class Account(BaseDefaults, Base):

    protocol = Column(String(128))
    identifier = Column(String(256))
    contact_id = Column(Integer, ForeignKey(Contact.id))

    contact = relationship("Contact", back_populates="protocols")
    conversations = relationship("Conversation", secondary=participants_table)


class Conversation(BaseDefaults, Base):

    title = Column(String(512))

    participants = relationship("Account", secondary=participants_table)
    messages = relationship("Message", back_populates="conversation")


class Message(BaseDefaults, Base):

    timestamp = Column(DateTime(timezone=True))
    body = Column(Text)

    sender_id = Column(Integer, ForeignKey(Account.id))
    conversation_id = Column(Integer, ForeignKey(Conversation.id))

    sender = relationship(Account)
    conversation = relationship(Conversation)
