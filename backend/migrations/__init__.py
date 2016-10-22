""" Help script to migrate database with scripts in this module. """

import importlib
from glob import glob
import os

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import MetaData, Table

from backend.models import Base
from backend.db import engine, Session


migration_directory = os.path.dirname(__file__)


class SchemaMigration(Base):
    __tablename__ = "schema_migrations"

    timestamp = Column(String(14), primary_key=True)
    name = Column(String(256))
    # applied_at = Column(Datetime(), auto_now=True)


# TODO: Create table in DB if it is missing
if not SchemaMigration.__table__.exists(bind=engine):
    print(type(SchemaMigration.__table__))
    SchemaMigration.__table__.create(bind=engine)
# TODO: Extract list from DB of applied migrations


def list_migrations():
    """ Return list of all migrations """

    session = Session()
    applied_migrations = (session.query(SchemaMigration)
                          .order_by("timestamp").all())
    migration_map = {m.timestamp: m for m in applied_migrations}

    filepattern = "[0-9]" * 14 + "_*.py"
    for filepath in glob(os.path.join(migration_directory, filepattern)):
        filename = os.path.basename(filepath)
        module_name, extension = os.path.splitext(filename)

        module = importlib.import_module("backend.migrations." + module_name)

        timestamp, name = module_name.split("_", maxsplit=1)
        title = ""

        if hasattr(module, "__doc__") and module.__doc__:
            doc_lines = module.__doc__.strip().split("\n")
            title = doc_lines[0].strip()

        if not hasattr(module, "name"):
            setattr(module, "name", name)

        if not hasattr(module, "title"):
            setattr(module, "title", title)

        if not hasattr(module, "timestamp"):
            setattr(module, "timestamp", timestamp)

        if not hasattr(module, "is_applied"):
            setattr(module, "is_applied", timestamp in migration_map)

        yield module


def display_migrations():
    for migration in list_migrations():
        applied = "*" if migration.is_applied else " "
        parts = ""
        if hasattr(migration, "remove"):
            parts += "<"
        else:
            parts += " "
        if hasattr(migration, "apply"):
            parts += ">"
        else:
            parts += " "

        print(" %s | %14s | %s | %-20s | %s" %
              (applied, migration.timestamp, parts,
               migration.name[:20], migration.title))


def apply():
    """ Try to apply all migrations not applied """
    pass

   # for migration in list_migrations():
   #     migration.apply(migration_engine)


def remove(until):
    """ Try to remove all migrations until given TS """
    pass

   # for migration in list_migrations():
   #     migration.remove(migration_engine)

