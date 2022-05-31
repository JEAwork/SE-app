import string
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from.database import Base

class Post(Base):
    __tablename__="posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content =  Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, 
                        server_default=text('Now()'))

class User(Base):
    __tablename__="users"
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, 
                        server_default=text('Now()'))

