from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str
    location: Dict[str, float]  # lat, lng
    area: float = Field(..., description="Area in hectares")
    start_date: datetime
    end_date: datetime
    status: str = Field(..., description="Project status: Planning, Active, Completed, On Hold")
    target_species: List[str]
    budget: float

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None

class ProjectInDB(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completion_percentage: float = 0.0
    actual_cost: float = 0.0

    class Config:
        orm_mode = True

class Project(ProjectInDB):
    pass

class ProjectMetrics(BaseModel):
    area_restored: float
    vegetation_survival_rate: float
    water_efficiency: float
    carbon_sequestration: float
    biodiversity_index: float

class ProjectTimeline(BaseModel):
    phase: str
    start_date: datetime
    end_date: datetime
    status: str
    deliverables: List[str]

class ResourcePlan(BaseModel):
    robots_required: Dict[str, int]
    water_requirements: Dict[str, float]
    seed_requirements: Dict[str, int]
    estimated_costs: Dict[str, float]

class SiteConditions(BaseModel):
    terrain_type: str
    average_temperature: float
    annual_rainfall: float
    soil_analysis: Dict[str, any]
    wind_conditions: Dict[str, any] 