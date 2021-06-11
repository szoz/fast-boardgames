from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship

from database import Base

boardgame_categories = Table('boardgame_categories', Base.metadata,
                             Column('id', Integer, nullable=False, primary_key=True),
                             Column('boardgame_id', Integer, ForeignKey('boardgames.id')),
                             Column('category_id', Integer, ForeignKey('categories.id')))


class Categories(Base):
    """Boardgame category database model."""
    __tablename__ = 'categories'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String)
    boardgames = relationship('Boardgames', secondary=boardgame_categories, back_populates='categories')


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
    categories = relationship('Categories', secondary=boardgame_categories, back_populates='boardgames')


class Users(Base):
    """User database model."""
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
