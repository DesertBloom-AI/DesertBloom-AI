from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.vegetation import (
    Species,
    VegetationScheme,
    MaintenanceRecord,
)
from app.schemas.vegetation import (
    SpeciesCreate,
    SpeciesUpdate,
    VegetationSchemeCreate,
    VegetationSchemeUpdate,
    MaintenanceRecordCreate,
    MaintenanceRecordUpdate,
)

class CRUDSpecies(CRUDBase[Species, SpeciesCreate, SpeciesUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Species]:
        return db.query(Species).filter(Species.name == name).first()

    def get_by_scientific_name(
        self, db: Session, *, scientific_name: str
    ) -> Optional[Species]:
        return db.query(Species).filter(Species.scientific_name == scientific_name).first()

    def get_by_type(
        self, db: Session, *, type: str, skip: int = 0, limit: int = 100
    ) -> List[Species]:
        return (
            db.query(Species)
            .filter(Species.type == type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: SpeciesCreate) -> Species:
        db_obj = Species(
            name=obj_in.name,
            scientific_name=obj_in.scientific_name,
            type=obj_in.type,
            description=obj_in.description,
            growth_rate=obj_in.growth_rate,
            water_requirement=obj_in.water_requirement,
            sunlight_requirement=obj_in.sunlight_requirement,
            temperature_range=obj_in.temperature_range,
            metadata=obj_in.metadata,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDVegetationScheme(CRUDBase[VegetationScheme, VegetationSchemeCreate, VegetationSchemeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[VegetationScheme]:
        return db.query(VegetationScheme).filter(VegetationScheme.name == name).first()

    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[VegetationScheme]:
        return (
            db.query(VegetationScheme)
            .filter(VegetationScheme.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[VegetationScheme]:
        return (
            db.query(VegetationScheme)
            .filter(VegetationScheme.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: VegetationSchemeCreate) -> VegetationScheme:
        db_obj = VegetationScheme(
            name=obj_in.name,
            description=obj_in.description,
            status=obj_in.status,
            progress=obj_in.progress,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            area=obj_in.area,
            species_composition=obj_in.species_composition,
            metadata=obj_in.metadata,
            project_id=obj_in.project_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_progress(
        self, db: Session, *, db_obj: VegetationScheme, progress: float
    ) -> VegetationScheme:
        db_obj.progress = progress
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(
        self, db: Session, *, db_obj: VegetationScheme, status: str
    ) -> VegetationScheme:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDMaintenanceRecord(CRUDBase[MaintenanceRecord, MaintenanceRecordCreate, MaintenanceRecordUpdate]):
    def get_by_scheme(
        self, db: Session, *, scheme_id: int, skip: int = 0, limit: int = 100
    ) -> List[MaintenanceRecord]:
        return (
            db.query(MaintenanceRecord)
            .filter(MaintenanceRecord.scheme_id == scheme_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type(
        self, db: Session, *, type: str, skip: int = 0, limit: int = 100
    ) -> List[MaintenanceRecord]:
        return (
            db.query(MaintenanceRecord)
            .filter(MaintenanceRecord.type == type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[MaintenanceRecord]:
        return (
            db.query(MaintenanceRecord)
            .filter(MaintenanceRecord.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: MaintenanceRecordCreate) -> MaintenanceRecord:
        db_obj = MaintenanceRecord(
            scheme_id=obj_in.scheme_id,
            date=obj_in.date,
            type=obj_in.type,
            description=obj_in.description,
            performed_by=obj_in.performed_by,
            status=obj_in.status,
            metadata=obj_in.metadata,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

species = CRUDSpecies(Species)
vegetation_scheme = CRUDVegetationScheme(VegetationScheme)
maintenance_record = CRUDMaintenanceRecord(MaintenanceRecord) 