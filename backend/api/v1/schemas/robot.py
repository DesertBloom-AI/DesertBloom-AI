from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime

class RobotBase(BaseModel):
    name: str
    type: str  # Seeder, Guardian, Collector
    status: str
    location: Dict[str, float]  # lat, lng
    battery_level: float
    current_task: Optional[str] = None
    sensor_data: Dict[str, float]

class RobotCreate(RobotBase):
    pass

class RobotUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    battery_level: Optional[float] = None
    current_task: Optional[str] = None
    sensor_data: Optional[Dict[str, float]] = None

class RobotInDB(RobotBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Robot(RobotInDB):
    pass

class RobotStatus(BaseModel):
    battery_level: float
    current_location: Dict[str, float]
    current_task: str
    system_health: str
    sensor_readings: Dict[str, float]

class RobotPath(BaseModel):
    waypoints: list[Dict[str, float]]
    estimated_time: float
    total_distance: float 