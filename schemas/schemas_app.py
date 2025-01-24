from pydantic import BaseModel
from typing import List, Optional


# Схема для Building
class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

class BuildingOut(BuildingBase):
    id: int

    class Config:
        from_attributes = True


# Схема для Activity
class ActivityBase(BaseModel):
    name: str
    parent_id: int

class ActivityOut(ActivityBase):
    id: int

    class Config:
        from_attributes = True


# Схема для Organization
class OrganizationBase(BaseModel):
    name: str
    phone_numbers: List[str]
    building_id: int
    activity_ids: List[int]



class OrganizationOut(OrganizationBase):
    id: int
    building: BuildingOut
    activities: List[ActivityOut]

    class Config:
        from_attributes = True

class OrganizationCreate(OrganizationBase):
    pass

class BuildingCreate(BuildingBase):
    pass

class ActivityCreate(ActivityBase):
    pass
