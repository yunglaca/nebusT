from pydantic import BaseModel
from typing import List, Optional


# Схема для Building
class Building(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
