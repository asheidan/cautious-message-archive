""" Help script to migrate database with scripts in this module. """

from datetime import datetime
import importlib
from glob import glob
import os

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Table

from backend.db import engine, Session
from backend.models import Base


migration_directory = os.path.dirname(__file__)

migration_template = os.path.join(migration_directory, "__template__.txt")


def add_column_to_table(table, column):
    engine = None
    if table.metadata.is_bound():
        engine = table.metadata.bind

    table_name = table.name

    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(dialect=engine.dialect)

    query_string = "ALTER TABLE %s ADD COLUMN %s %s " % (
        table_name, column_name, column_type
    )
    print(query_string)
    engine.execute(query_string)

Table.add_column = add_column_to_table


class SchemaMigration(Base):
    __tablename__ = "schema_migrations"

    timestamp = Column(String(14), primary_key=True)
    name = Column(String(256))
    # applied_at = Column(Datetime(), auto_now=True)


# TODO: Create table in DB if it is missing
if not SchemaMigration.__table__.exists(bind=engine):
    print("Table for migrations was not found, will create now...")
    SchemaMigration.__table__.create(bind=engine)

migration_engine = engine


def list_migrations():
    """ Return list of all migrations """

    # Extract list from DB of applied migrations
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


def display_migrations(args):
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


def apply_migrations(args):
    """ Try to apply all migrations not applied """
    # TODO: Find better name than apply

    for migration in list_migrations():
        if not migration.is_applied:
            if not hasattr(migration, "apply"):
                raise Exception("Missing code for applying migration.")
            migration.apply(migration_engine)
            session = Session()
            session.add(SchemaMigration(timestamp=migration.timestamp,
                                        name=migration.name))
            session.commit()
            session.close()


def remove_migrations(until):
    """ Try to remove all migrations until given TS """

    for migration in list_migrations():
        if migration.is_applied:
            if not hasattr(migration, "remove"):
                raise Exception("Missing code for removing migration.")
            migration.remove(migration_engine)
            session = Session()
            (session.query(SchemaMigration)
             .filter(SchemaMigration.timestamp == migration.timestamp)
             .delete())


def create_migration(args):
    """ Create a new migration from template """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.py" % (timestamp, args.migration_name)
    filepath = os.path.join(migration_directory, filename)
    with open(migration_template, "r") as template_file:
        template = template_file.read()
        with open(filepath, "w") as migration_file:
            migration_file.write(template)

            print("A new migration has been created: %s" %
                  filepath)
