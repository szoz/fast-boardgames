from pydantic import BaseModel


def to_camel(string: str):
    """Schema helper function to export models with camelCase properties."""
    pascal_cased = ''.join(word.capitalize() for word in string.split('_'))
    return f'{pascal_cased[0].lower()}{pascal_cased[1:]}'


class ConfiguredModel(BaseModel):
    """Class with configuration for all schemas."""

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class Category(ConfiguredModel):
    """Boardgame category schema."""
    id: int
    name: str
