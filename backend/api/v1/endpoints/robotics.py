from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from ..services.robotics_service import RoboticsService
from ..schemas.robotics import (
    RobotConfig,
    Task,
    TaskResult,
    RobotStatus,
    TaskQueue,
    EmergencyStop,
    RobotHealth
)

router = APIRouter()
robotics_service = RoboticsService()

@router.post("/robots/{robot_id}/initialize", response_model=RobotConfig)
async def initialize_robot(robot_id: str):
    """Initialize a robot"""
    try:
        return robotics_service.initialize_robot(robot_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/robots/{robot_id}/tasks", response_model=bool)
async def assign_task(robot_id: str, task: Task):
    """Assign a task to a robot"""
    try:
        return robotics_service.assign_task(robot_id, task.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/robots/{robot_id}/tasks/execute", response_model=TaskResult)
async def execute_task(robot_id: str, task: Task):
    """Execute a task with a robot"""
    try:
        return robotics_service.execute_task(robot_id, task.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/robots/{robot_id}/status", response_model=RobotStatus)
async def get_robot_status(robot_id: str):
    """Get current status of a robot"""
    try:
        return robotics_service.get_robot_status(robot_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/tasks/queue", response_model=TaskQueue)
async def get_task_queue():
    """Get current task queue"""
    tasks = robotics_service.get_task_queue()
    return TaskQueue(
        tasks=tasks,
        total_tasks=len(tasks),
        pending_tasks=len([t for t in tasks if t['status'] == 'pending']),
        in_progress_tasks=len([t for t in tasks if t['status'] == 'in_progress']),
        completed_tasks=len([t for t in tasks if t['status'] == 'completed'])
    )

@router.post("/robots/{robot_id}/emergency_stop", response_model=bool)
async def emergency_stop(robot_id: str, reason: str = None):
    """Emergency stop a robot"""
    try:
        return robotics_service.emergency_stop(robot_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/robots/{robot_id}/health", response_model=RobotHealth)
async def get_robot_health(robot_id: str):
    """Get robot health status"""
    try:
        status = robotics_service.get_robot_status(robot_id)
        return RobotHealth(
            robot_id=robot_id,
            battery_health=status['battery_level'],
            motor_health=95.0,  # Example value
            sensor_health=98.0,  # Example value
            last_maintenance="2024-01-01T00:00:00",  # Example value
            next_maintenance="2024-02-01T00:00:00"   # Example value
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/robots/{robot_id}/position", response_model=bool)
async def update_robot_position(robot_id: str, position: Dict):
    """Update robot position"""
    try:
        robotics_service.update_robot_position(robot_id, position)
        return True
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/robots/{robot_id}/battery", response_model=bool)
async def update_robot_battery(robot_id: str, battery_level: float):
    """Update robot battery level"""
    try:
        robotics_service.update_robot_battery(robot_id, battery_level)
        return True
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 