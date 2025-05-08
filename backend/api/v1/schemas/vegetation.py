from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VegetationBase(BaseModel):
    species: str
    scientific_name: str
    planting_date: datetime
    location: dict
    status: str
    health_index: float
    growth_rate: float
    water_consumption: float

class VegetationCreate(VegetationBase):
    pass

class VegetationUpdate(BaseModel):
    species: Optional[str] = None
    scientific_name: Optional[str] = None
    status: Optional[str] = None
    health_index: Optional[float] = None
    growth_rate: Optional[float] = None
    water_consumption: Optional[float] = None

class VegetationInDB(VegetationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Vegetation(VegetationInDB):
    pass 