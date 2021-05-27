from sqlalchemy import Column, String, Integer

from database import Base


class Category(Base):
    """Boardgame category database model."""
    __tablename__ = 'categories'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String)
