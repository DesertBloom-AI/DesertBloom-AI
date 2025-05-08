from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Robot])
def read_robots(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve robots.
    """
    if crud.user.is_superuser(current_user):
        robots = crud.robot.get_multi(db, skip=skip, limit=limit)
    else:
        robots = crud.robot.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return robots

@router.post("/", response_model=schemas.Robot)
def create_robot(
    *,
    db: Session = Depends(deps.get_db),
    robot_in: schemas.RobotCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new robot.
    """
    project = crud.project.get(db=db, id=robot_in.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if not crud.user.is_superuser(current_user):
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    robot = crud.robot.create(db=db, obj_in=robot_in)
    return robot

@router.get("/{robot_id}", response_model=schemas.Robot)
def read_robot(
    *,
    db: Session = Depends(deps.get_db),
    robot_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get robot by ID.
    """
    robot = crud.robot.get(db=db, id=robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=robot.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    return robot

@router.put("/{robot_id}", response_model=schemas.Robot)
def update_robot(
    *,
    db: Session = Depends(deps.get_db),
    robot_id: int,
    robot_in: schemas.RobotUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update robot.
    """
    robot = crud.robot.get(db=db, id=robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=robot.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    robot = crud.robot.update(db=db, db_obj=robot, obj_in=robot_in)
    return robot

@router.delete("/{robot_id}", response_model=schemas.Robot)
def delete_robot(
    *,
    db: Session = Depends(deps.get_db),
    robot_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete robot.
    """
    robot = crud.robot.get(db=db, id=robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=robot.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    robot = crud.robot.remove(db=db, id=robot_id)
    return robot

@router.post("/{robot_id}/tasks/", response_model=schemas.RobotTask)
def create_robot_task(
    *,
    db: Session = Depends(deps.get_db),
    robot_id: int,
    task_in: schemas.RobotTaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task for robot.
    """
    robot = crud.robot.get(db=db, id=robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=robot.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    task = crud.robot_task.create_with_robot(
        db=db, obj_in=task_in, robot_id=robot_id
    )
    return task

@router.get("/{robot_id}/tasks/", response_model=List[schemas.RobotTask])
def read_robot_tasks(
    *,
    db: Session = Depends(deps.get_db),
    robot_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all tasks for a robot.
    """
    robot = crud.robot.get(db=db, id=robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=robot.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    tasks = crud.robot_task.get_multi_by_robot(
        db=db, robot_id=robot_id, skip=skip, limit=limit
    )
    return tasks 