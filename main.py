from fastapi import FastAPI
from routes.cats_routes import router as cats_router
from routes.missions_routes import router as missions_router
from routes.target_routes import router as targets_router

app = FastAPI(
    title="Spy Cats API",
    description="API for managing spy cats, missions, and targets.",
    version="1.0.0"
)

app.include_router(cats_router)
app.include_router(missions_router)
app.include_router(targets_router)