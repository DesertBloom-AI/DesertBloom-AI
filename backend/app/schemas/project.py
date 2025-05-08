from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ProjectStatus(str, Enum):
    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
    area: float
    status: str = "planning"
    is_active: bool = True
    metadata: Optional[Dict] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    location: Optional[str] = None
    area: Optional[float] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class ProjectInDBBase(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass

class ProjectInDB(ProjectInDBBase):
    pass

class MilestoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.PLANNING
    progress: float = 0.0
    due_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class MilestoneCreate(MilestoneBase):
    project_id: int

class MilestoneUpdate(MilestoneBase):
    name: Optional[str] = None
    project_id: Optional[int] = None

class MilestoneInDBBase(MilestoneBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Milestone(MilestoneInDBBase):
    pass

class MilestoneInDB(MilestoneInDBBase):
    pass 