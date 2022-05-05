from database.db_connection import Base
from sqlalchemy import Column, Integer, String, Date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    created_on = Column(Date)
    role_id = Column(String)


class Role(Base):
    __tablename__ = 'role'

    id_role = Column(Integer, primary_key=True, index=True)
    role_name = Column(String)


class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String)
    user_id = Column(Integer)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    post = Column(String)
    created_on = Column(Date)
    tag_id = Column(Integer)
    user_id = Column(Integer)
