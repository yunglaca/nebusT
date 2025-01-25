from pydantic import BaseModel, model_validator
from typing import List, Optional

class ActivityBase(BaseModel):
    id: int
    name: str

    class Config:
        from_orm = True

class ActivitySchema(ActivityBase):
    parent: Optional["ActivitySchema"] = None
    children: List["ActivitySchema"] = []

    @model_validator(mode='before')
    def remove_recursive_fields(cls, values):
        # Преобразуем values в словарь и удаляем рекурсивные поля
        values_dict = values if isinstance(values, dict) else values.__dict__  
        values_dict.pop("parent", None)
        values_dict.pop("children", None)
        return values_dict

    class Config:
        from_orm = True
        from_attributes = True
