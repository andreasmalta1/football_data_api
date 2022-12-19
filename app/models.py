from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

try:
    from .database import Base
except ImportError:
    from database import Base


class Post(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, nullable=False)
    img = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
