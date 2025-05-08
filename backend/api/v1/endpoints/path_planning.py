from fastapi import APIRouter, HTTPException
from typing import List, Dict
from ..services.path_planning import PathPlanningService
from ..schemas.robotics import RobotPosition
import json

router = APIRouter()
path_planning_service = PathPlanningService()

@router.post("/robots/{robot_id}/path", response_model=List[Dict])
async def plan_path(robot_id: str, start: RobotPosition, goal: RobotPosition):
    """Plan a path for a robot from start to goal"""
    try:
        path = path_planning_service.plan_path(
            start.dict(),
            goal.dict(),
            robot_id
        )
        if not path:
            raise HTTPException(status_code=404, detail="No valid path found")
        return path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/robots/{robot_id}/path/optimize", response_model=List[Dict])
async def optimize_path(robot_id: str, path: List[Dict]):
    """Optimize a path for smoother movement"""
    try:
        return path_planning_service.optimize_path(path, robot_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/robots/{robot_id}/collision", response_model=bool)
async def check_collision(robot_id: str, position: RobotPosition):
    """Check if a position would cause a collision"""
    try:
        return path_planning_service.check_collision(
            position.dict(),
            robot_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/map/zones", response_model=List[Dict])
async def get_zones():
    """Get all zones in the map"""
    try:
        with open('robotics/config/map_data.json') as f:
            map_data = json.load(f)
        return map_data['zones']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/map/obstacles", response_model=List[Dict])
async def get_obstacles():
    """Get all obstacles in the map"""
    try:
        with open('robotics/config/map_data.json') as f:
            map_data = json.load(f)
        return map_data['obstacles']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/map/charging_stations", response_model=List[Dict])
async def get_charging_stations():
    """Get all charging stations in the map"""
    try:
        with open('robotics/config/map_data.json') as f:
            map_data = json.load(f)
        return map_data['charging_stations']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/map/paths", response_model=List[Dict])
async def get_paths():
    """Get all predefined paths in the map"""
    try:
        with open('robotics/config/map_data.json') as f:
            map_data = json.load(f)
        return map_data['paths']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 