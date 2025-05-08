from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() 

# Import all models here
from app.models.user import User
from app.models.project import Project
from app.models.robot import Robot
from app.models.vegetation import Vegetation 