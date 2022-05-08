from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
import sqlalchemy


DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    surname = Column('surname', String)
    name = Column('name', String)
    patronymic = Column('patronymic', String)
    phone = Column('phone', String)
    email = Column('email', String)
    password = Column('password', String)
    is_admin = Column('is_admin', Boolean)
    tasks = orm.relation("Task", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Task(DeclarativeBase):
    __tablename__ = 'tasks'

    id = Column('id', Integer, primary_key=True)
    task_type = Column('task_type', Integer)
    user_id = Column('user_id', Integer, sqlalchemy.ForeignKey("users.id"))
    is_finished = Column('is_finished', Boolean)
    inf = Column('inf', JSON)
    user = orm.relation('User')


class Place(DeclarativeBase):
    __tablename__ = 'places'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)


class Equipment(DeclarativeBase):
    __tablename__ = 'equipment'

    id = Column('id', Integer, primary_key=True)
    type = Column('type', Integer)
    group = Column('group', Integer)
    nums_list = Column('nums_list', String)
    name = Column('name', String)
    place = Column('place', String)


class EquipmentGroup(DeclarativeBase):
    __tablename__ = 'equipment_group'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    num = Column('num', Integer)


class EquipmentType(DeclarativeBase):
    __tablename__ = 'equipment_type'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)