from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import (
    auth,
    users,
    plants,
    sensors,
    irrigation,
    analytics,
    robotics,
    path_planning
)

app = FastAPI(
    title="DesertBloom AI API",
    description="API for DesertBloom AI - Smart Desert Agriculture System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(plants.router, prefix="/api/v1", tags=["Plants"])
app.include_router(sensors.router, prefix="/api/v1", tags=["Sensors"])
app.include_router(irrigation.router, prefix="/api/v1", tags=["Irrigation"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(robotics.router, prefix="/api/v1", tags=["Robotics"])
app.include_router(path_planning.router, prefix="/api/v1", tags=["Path Planning"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to DesertBloom AI API",
        "version": "1.0.0",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 