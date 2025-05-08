from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RobotPosition(BaseModel):
    x: float
    y: float
    z: float

class RobotOrientation(BaseModel):
    x: float
    y: float
    z: float
    w: float

class RobotStatus(BaseModel):
    status: str
    battery_level: float = Field(..., ge=0, le=100)
    position: RobotPosition
    orientation: RobotOrientation
    last_update: datetime
    current_task: Optional[Dict] = None

class RobotConfig(BaseModel):
    robot_id: str
    type: str
    capabilities: List[str]
    status: str

class Task(BaseModel):
    id: str
    type: str
    priority: int = Field(..., ge=1, le=5)
    area: float
    parameters: Dict

class PlantingTask(Task):
    type: str = "planting"
    quantity: int
    species: str
    spacing: float

class WateringTask(Task):
    type: str = "watering"
    water_amount: float
    duration: int
    frequency: int

class MonitoringTask(Task):
    type: str = "monitoring"
    sensors: List[str]
    interval: int
    duration: int

class TaskResult(BaseModel):
    robot_id: str
    task_id: str
    status: str
    start_time: datetime
    completion_percentage: float = Field(..., ge=0, le=100)
    metrics: Dict

class PlantingResult(TaskResult):
    plants_planted: int
    area_covered: float

class WateringResult(TaskResult):
    water_used: float
    area_watered: float

class MonitoringResult(TaskResult):
    data_collected: Dict
    area_monitored: float

class TaskQueue(BaseModel):
    tasks: List[Dict]
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int

class EmergencyStop(BaseModel):
    robot_id: str
    timestamp: datetime
    reason: Optional[str] = None

class RobotHealth(BaseModel):
    robot_id: str
    battery_health: float = Field(..., ge=0, le=100)
    motor_health: float = Field(..., ge=0, le=100)
    sensor_health: float = Field(..., ge=0, le=100)
    last_maintenance: datetime
    next_maintenance: datetime 