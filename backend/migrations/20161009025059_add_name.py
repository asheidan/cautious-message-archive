""" Nisse är en liten apa"""

from sqlalchemy import Table, MetaData, Column, String


def apply(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    contacts_table = Table("contacts", meta, autoload=True)
    name_column = Column("name", String(256))
    name_column.create(contacts_table)


def remove(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    contacts_table = Table("contacts", meta, autoload=True)
    contacts_table.c.name.drop()
