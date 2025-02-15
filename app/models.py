# 3RD PARTY IMPORTS
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

# LOCAL IMPORTS
from .database import Base




# Posts DB Model Setting
class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = False, server_default = 'True')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = 'NOW()')
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    



# Users DB Model Setting
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = 'NOW()')
    




















