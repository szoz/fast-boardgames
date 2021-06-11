from pydantic import BaseModel, PositiveInt, EmailStr
from enum import Enum
from typing import List


def to_camel(string: str):
    """Schema helper function to export models with camelCase properties."""
    pascal_cased = ''.join(word.capitalize() for word in string.split('_'))
    return f'{pascal_cased[0].lower()}{pascal_cased[1:]}'


class BoardgameSortEnum(str, Enum):
    """Enumerator with boardgame sorting criteria."""
    score = 'score'
    score_ = '-score'
    complexity = 'complexity'
    complexity_ = '-complexity'
    name = 'name'
    name_ = '-name'


class BoardgameComplexityEnum(Enum):
    """Enumerator with boardgame complexity level."""
    value_1 = 'simple'
    value_2 = 'easy'
    value_3 = 'medium'
    value_4 = 'hard'

    @property
    def minimum(self):
        """Return minimum complexity value for given complexity level."""
        return int(self.name[-1:])

    @property
    def maximum(self):
        """Return maximum complexity value for given complexity level."""
        return int(self.name[-1:]) + 1


class ConfiguredModel(BaseModel):
    """Class with configuration for all schemas."""

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class Category(ConfiguredModel):
    """Boardgame category schema."""
    id: PositiveInt
    name: str


class Boardgame(ConfiguredModel):
    """Boardgame schema."""
    id: PositiveInt
    name: str
    year: int
    score: float
    complexity: float
    brief: str
    description: str
    categories: List[Category]


class User(ConfiguredModel):
    """User without password schema."""
    name: str
    email: EmailStr
