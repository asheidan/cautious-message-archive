""" Create table for the Account model """

from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey

meta = MetaData()

accounts_table = Table(
    "accounts", meta,
    Column("id", Integer, primary_key=True),
    Column("protocol", String(128)),
    Column("identifier", String(256)),
    Column("contact_id", Integer, ForeignKey("contacts.id"))
)


def apply(migration_engine):
    meta.bind = migration_engine
    meta.reflect()

    accounts_table.create()


def remove(migration_engine):
    meta.bind = migration_engine
    meta.reflect()

    accounts_table.drop()
