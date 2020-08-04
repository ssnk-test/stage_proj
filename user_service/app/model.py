import asyncpgsa
from sqlalchemy import MetaData, Table, Column,String

metadata = MetaData()

users = Table(
    "user",
    metadata,
    Column("username", String(20), nullable=False, unique=True),
    Column("email", String(20), nullable=True, unique=True),
    Column("password", String(200), nullable=False)
)