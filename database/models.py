from database.db_connection import Base
from sqlalchemy import Column, Integer, String, Date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    created_on = Column(Date)
    role_id = Column(String)


class Role(Base):
    __tablename__ = 'role'

    id_role = Column(Integer, primary_key=True, index=True)
    role_name = Column(String)
