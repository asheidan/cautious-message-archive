""" Nisse är en liten apa"""

from sqlalchemy import Table, MetaData, Column, String


def apply(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    contacts_table = Table("contacts", meta, autoload=True)
    name_column = Column("name", String(256))
    contacts_table.add_column(name_column)
