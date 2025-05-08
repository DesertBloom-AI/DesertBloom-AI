from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, projects, robots, vegetation, blockchain, login

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(robots.router, prefix="/robots", tags=["robots"])
api_router.include_router(vegetation.router, prefix="/vegetation", tags=["vegetation"])
api_router.include_router(blockchain.router, prefix="/blockchain", tags=["blockchain"])
api_router.include_router(login.router, tags=["login"]) 