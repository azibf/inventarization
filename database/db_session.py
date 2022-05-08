from database.tables import *
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session


__factory = None
DATABASE = {
    'drivername': 'postgresql',
    'host': 'ec2-3-208-157-78.compute-1.amazonaws.com',
    'port': '5432',
    'username': 'kaklftywrejano',
    'password': '90342d2e6247133991fefb9ea6a0a2be1fdca58b4666a478948b4cf245729f95',
    'database': 'd16vjob824aaqb'
}


def global_init():
    global __factory
    if __factory:
        return
    engine = create_engine(URL(**DATABASE))
    DeclarativeBase.metadata.create_all(engine)
    __factory = sessionmaker(bind=engine)


def create_session() -> Session:
    global __factory
    return __factory()
