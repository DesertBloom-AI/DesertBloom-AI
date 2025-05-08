from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DesertBloom AI"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./desertbloom.db"

    class Config:
        case_sensitive = True

settings = Settings() 