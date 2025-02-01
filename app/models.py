# 3RD PARTY IMPORTS
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

# LOCAL IMPORTS
from .database import Base


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = False, server_default = 'True')
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = 'NOW()')
    
























