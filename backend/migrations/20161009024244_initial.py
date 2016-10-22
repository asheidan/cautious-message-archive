""" Initial commits of basic models. """

from sqlalchemy import Table, MetaData, Column, Integer

meta = MetaData()

contacts_table = Table(
    "contacts", meta,
    Column("id", Integer, primary_key=True)
)


def apply(migrate_engine):
    meta.bind = migrate_engine
    contacts_table.create()


def remove(migrate_engine):
    meta.bind = migrate_engine
    contacts_table.drop()
