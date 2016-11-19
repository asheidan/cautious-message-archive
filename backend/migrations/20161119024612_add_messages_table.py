""" Add table for the Message model """

from sqlalchemy import Table, MetaData, Column, ForeignKey
from sqlalchemy import Integer, DateTime, Text

meta = MetaData()

messages_table = Table(
    "messages", meta,
    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime(timezone=True)),
    Column("body", Text),

    Column("sender_id", Integer, ForeignKey("accounts.id")),
    Column("conversation_id", Integer, ForeignKey("conversations.id")),
)


def apply(migration_engine):
    meta.bind = migration_engine
    meta.reflect()

    messages_table.create()


def remove(migration_engine):
    meta.bind = migration_engine
    meta.reflect()

    messages_table.drop()
