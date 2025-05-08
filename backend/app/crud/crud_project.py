from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.project import Project, Milestone
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    MilestoneCreate,
    MilestoneUpdate,
)

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Project]:
        return db.query(Project).filter(Project.name == name).first()

    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Project]:
        return db.query(Project).filter(Project.is_active == True).offset(skip).limit(limit).all()

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return (
            db.query(Project)
            .filter(Project.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return (
            db.query(Project)
            .filter(Project.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        db_obj = Project(
            name=obj_in.name,
            description=obj_in.description,
            status=obj_in.status,
            progress=obj_in.progress,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            budget=obj_in.budget,
            metadata=obj_in.metadata,
            user_id=obj_in.user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDMilestone(CRUDBase[Milestone, MilestoneCreate, MilestoneUpdate]):
    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Milestone]:
        return (
            db.query(Milestone)
            .filter(Milestone.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Milestone]:
        return (
            db.query(Milestone)
            .filter(Milestone.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: MilestoneCreate) -> Milestone:
        db_obj = Milestone(
            name=obj_in.name,
            description=obj_in.description,
            status=obj_in.status,
            progress=obj_in.progress,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            metadata=obj_in.metadata,
            project_id=obj_in.project_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

project = CRUDProject(Project)
milestone = CRUDMilestone(Milestone) 