from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#using-a-memory-database-in-multiple-threads

engine = create_engine("sqlite:///test.db", echo=True, poolclass=StaticPool)

Session = sessionmaker(bind=engine)
