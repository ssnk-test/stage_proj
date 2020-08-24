#import asyncpgsa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,String

Base = declarative_base(metadata=MetaData())


class Users(Base):
    __tablename__ = "users_table"

    username = Column(String, nullable=False, unique=True)
    uuid = Column(String,primary_key=True, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)