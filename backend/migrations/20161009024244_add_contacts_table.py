""" Add table for the Contact model """

from sqlalchemy import Table, MetaData, Column, Integer, String

meta = MetaData()

contacts_table = Table(
    "contacts", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(256)),
    Column("nickname", String(256)),
)


def apply(migrate_engine):
    meta.bind = migrate_engine
    contacts_table.create()


def remove(migrate_engine):
    meta.bind = migrate_engine
    contacts_table.drop()
