from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.robot import Robot, RobotTask
from app.schemas.robot import (
    RobotCreate,
    RobotUpdate,
    RobotTaskCreate,
    RobotTaskUpdate,
)

class CRUDRobot(CRUDBase[Robot, RobotCreate, RobotUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Robot]:
        return db.query(Robot).filter(Robot.name == name).first()

    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Robot]:
        return (
            db.query(Robot)
            .filter(Robot.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Robot]:
        return (
            db.query(Robot)
            .filter(Robot.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: RobotCreate) -> Robot:
        db_obj = Robot(
            name=obj_in.name,
            model=obj_in.model,
            status=obj_in.status,
            battery_level=obj_in.battery_level,
            location=obj_in.location,
            current_task=obj_in.current_task,
            metadata=obj_in.metadata,
            project_id=obj_in.project_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_battery_level(
        self, db: Session, *, db_obj: Robot, battery_level: float
    ) -> Robot:
        db_obj.battery_level = battery_level
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_location(
        self, db: Session, *, db_obj: Robot, location: Dict[str, Any]
    ) -> Robot:
        db_obj.location = location
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(
        self, db: Session, *, db_obj: Robot, status: str
    ) -> Robot:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDRobotTask(CRUDBase[RobotTask, RobotTaskCreate, RobotTaskUpdate]):
    def get_by_robot(
        self, db: Session, *, robot_id: int, skip: int = 0, limit: int = 100
    ) -> List[RobotTask]:
        return (
            db.query(RobotTask)
            .filter(RobotTask.robot_id == robot_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[RobotTask]:
        return (
            db.query(RobotTask)
            .filter(RobotTask.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: RobotTaskCreate) -> RobotTask:
        db_obj = RobotTask(
            name=obj_in.name,
            description=obj_in.description,
            status=obj_in.status,
            progress=obj_in.progress,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time,
            metadata=obj_in.metadata,
            robot_id=obj_in.robot_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_progress(
        self, db: Session, *, db_obj: RobotTask, progress: float
    ) -> RobotTask:
        db_obj.progress = progress
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(
        self, db: Session, *, db_obj: RobotTask, status: str
    ) -> RobotTask:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

robot = CRUDRobot(Robot)
robot_task = CRUDRobotTask(RobotTask) 