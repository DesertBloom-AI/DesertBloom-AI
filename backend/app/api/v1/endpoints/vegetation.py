from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/species/", response_model=List[schemas.Species])
def read_species(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve species.
    """
    species = crud.species.get_multi(db, skip=skip, limit=limit)
    return species

@router.post("/species/", response_model=schemas.Species)
def create_species(
    *,
    db: Session = Depends(deps.get_db),
    species_in: schemas.SpeciesCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new species.
    """
    species = crud.species.create(db=db, obj_in=species_in)
    return species

@router.get("/species/{species_id}", response_model=schemas.Species)
def read_species_by_id(
    species_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific species by id.
    """
    species = crud.species.get(db=db, id=species_id)
    if not species:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Species not found",
        )
    return species

@router.put("/species/{species_id}", response_model=schemas.Species)
def update_species(
    *,
    db: Session = Depends(deps.get_db),
    species_id: int,
    species_in: schemas.SpeciesUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a species.
    """
    species = crud.species.get(db=db, id=species_id)
    if not species:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Species not found",
        )
    species = crud.species.update(db=db, db_obj=species, obj_in=species_in)
    return species

@router.get("/schemes/", response_model=List[schemas.VegetationScheme])
def read_schemes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve vegetation schemes.
    """
    if crud.user.is_superuser(current_user):
        schemes = crud.vegetation_scheme.get_multi(db, skip=skip, limit=limit)
    else:
        schemes = crud.vegetation_scheme.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return schemes

@router.post("/schemes/", response_model=schemas.VegetationScheme)
def create_scheme(
    *,
    db: Session = Depends(deps.get_db),
    scheme_in: schemas.VegetationSchemeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new vegetation scheme.
    """
    project = crud.project.get(db=db, id=scheme_in.project_id)
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
    scheme = crud.vegetation_scheme.create(db=db, obj_in=scheme_in)
    return scheme

@router.get("/schemes/{scheme_id}", response_model=schemas.VegetationScheme)
def read_scheme(
    *,
    db: Session = Depends(deps.get_db),
    scheme_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get vegetation scheme by ID.
    """
    scheme = crud.vegetation_scheme.get(db=db, id=scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vegetation scheme not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=scheme.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    return scheme

@router.put("/schemes/{scheme_id}", response_model=schemas.VegetationScheme)
def update_scheme(
    *,
    db: Session = Depends(deps.get_db),
    scheme_id: int,
    scheme_in: schemas.VegetationSchemeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update vegetation scheme.
    """
    scheme = crud.vegetation_scheme.get(db=db, id=scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vegetation scheme not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=scheme.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    scheme = crud.vegetation_scheme.update(db=db, db_obj=scheme, obj_in=scheme_in)
    return scheme

@router.post("/schemes/{scheme_id}/maintenance/", response_model=schemas.MaintenanceRecord)
def create_maintenance_record(
    *,
    db: Session = Depends(deps.get_db),
    scheme_id: int,
    record_in: schemas.MaintenanceRecordCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new maintenance record for vegetation scheme.
    """
    scheme = crud.vegetation_scheme.get(db=db, id=scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vegetation scheme not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=scheme.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    record = crud.maintenance_record.create_with_scheme(
        db=db, obj_in=record_in, scheme_id=scheme_id
    )
    return record

@router.get("/schemes/{scheme_id}/maintenance/", response_model=List[schemas.MaintenanceRecord])
def read_maintenance_records(
    *,
    db: Session = Depends(deps.get_db),
    scheme_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all maintenance records for a vegetation scheme.
    """
    scheme = crud.vegetation_scheme.get(db=db, id=scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vegetation scheme not found",
        )
    if not crud.user.is_superuser(current_user):
        project = crud.project.get(db=db, id=scheme.project_id)
        if not crud.project.is_user_project(db, project_id=project.id, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough permissions",
            )
    records = crud.maintenance_record.get_multi_by_scheme(
        db=db, scheme_id=scheme_id, skip=skip, limit=limit
    )
    return records 