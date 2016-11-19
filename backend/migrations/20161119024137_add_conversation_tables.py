""" Add tables for the Conversation model """

from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey

meta = MetaData()

conversations_table = Table(
    "conversations", meta,
    Column("id", Integer, primary_key=True),
    Column("title", String(512)),
)

participants_table = Table(
    'conversation_participants', meta,
    Column("account_id", Integer, ForeignKey("accounts.id")),
    Column("conversation_id", Integer, ForeignKey("conversations.id")))


def apply(migration_engine):
    meta.bind = migration_engine
    meta.reflect()

    conversations_table.create()
    participants_table.create()


def remove(migration_engine):
    meta.bind = migration_engine
    meta.reflect()

    participants_table.drop()
    conversations_table.drop()
