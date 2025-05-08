from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base
from app.api.v1.endpoints.projects import router as projects_router

# Create database tables
from app.db.init_db import init_db
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 包含路由
app.include_router(projects_router, prefix=settings.API_V1_STR + "/projects", tags=["projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to DesertBloom AI API"} 