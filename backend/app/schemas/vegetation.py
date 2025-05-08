from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class SpeciesType(str, Enum):
    TREE = "TREE"
    SHRUB = "SHRUB"
    GRASS = "GRASS"
    FLOWER = "FLOWER"

class SchemeStatus(str, Enum):
    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"

class SpeciesBase(BaseModel):
    name: str
    scientific_name: str
    type: SpeciesType
    description: Optional[str] = None
    growth_rate: float
    water_requirement: float
    sunlight_requirement: float
    temperature_range: Dict[str, float]
    metadata: Optional[Dict[str, Any]] = None

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesUpdate(SpeciesBase):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    type: Optional[SpeciesType] = None

class SpeciesInDBBase(SpeciesBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Species(SpeciesInDBBase):
    pass

class SpeciesInDB(SpeciesInDBBase):
    pass

class VegetationSchemeBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[SchemeStatus] = SchemeStatus.PLANNING
    progress: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    area: float
    species_composition: Dict[str, float]  # species_id: percentage
    metadata: Optional[Dict[str, Any]] = None

class VegetationSchemeCreate(VegetationSchemeBase):
    project_id: int

class VegetationSchemeUpdate(VegetationSchemeBase):
    name: Optional[str] = None
    project_id: Optional[int] = None

class VegetationSchemeInDBBase(VegetationSchemeBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VegetationScheme(VegetationSchemeInDBBase):
    pass

class VegetationSchemeInDB(VegetationSchemeInDBBase):
    pass

class MaintenanceRecordBase(BaseModel):
    scheme_id: int
    date: datetime
    type: str
    description: Optional[str] = None
    performed_by: str
    status: str
    metadata: Optional[Dict[str, Any]] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecordUpdate(MaintenanceRecordBase):
    scheme_id: Optional[int] = None
    date: Optional[datetime] = None

class MaintenanceRecordInDBBase(MaintenanceRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MaintenanceRecord(MaintenanceRecordInDBBase):
    pass

class MaintenanceRecordInDB(MaintenanceRecordInDBBase):
    pass 