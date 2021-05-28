from sqlalchemy import Column, String, Integer, Float

from database import Base


class Category(Base):
    """Boardgame category database model."""
    __tablename__ = 'categories'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String)


class Boardgames(Base):
    """Boardgame database model."""
    __tablename__ = 'boardgames'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    score = Column(Float)
    complexity = Column(Float)
    brief = Column(String)
    description = Column(String)
