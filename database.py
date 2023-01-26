import sqlalchemy
from sqlalchemy.ext import declarative
from sqlalchemy import orm 




DB_URL = "sqlite:///test.db"
engine = sqlalchemy.create_engine(DB_URL, connect_args={'check_same_thread' : False})


SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
















