from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class RobotStatus(str, Enum):
    IDLE = "IDLE"
    WORKING = "WORKING"
    MAINTENANCE = "MAINTENANCE"
    ERROR = "ERROR"

class RobotBase(BaseModel):
    name: str
    model: Optional[str] = None
    status: Optional[RobotStatus] = RobotStatus.IDLE
    battery_level: float = 100.0
    location: Optional[Dict[str, Any]] = None
    current_task: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RobotCreate(RobotBase):
    project_id: int

class RobotUpdate(RobotBase):
    name: Optional[str] = None
    project_id: Optional[int] = None

class RobotInDBBase(RobotBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Robot(RobotInDBBase):
    pass

class RobotInDB(RobotInDBBase):
    pass

class RobotTaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[RobotStatus] = RobotStatus.IDLE
    progress: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class RobotTaskCreate(RobotTaskBase):
    robot_id: int

class RobotTaskUpdate(RobotTaskBase):
    name: Optional[str] = None
    robot_id: Optional[int] = None

class RobotTaskInDBBase(RobotTaskBase):
    id: int
    robot_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RobotTask(RobotTaskInDBBase):
    pass

class RobotTaskInDB(RobotTaskInDBBase):
    pass 