from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.missions_schema import MissionCreate, MissionAssignCat, MissionResponse
from services.missions_service import (
    create_mission_with_targets,
    delete_mission,
    assign_cat_to_mission,
    list_missions,
    get_mission,
)
from db.db import get_db

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
async def create_mission(mission: MissionCreate, db: AsyncSession = Depends(get_db)):
    return await create_mission_with_targets(db, mission)

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_mission(mission_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await delete_mission(db, mission_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return

@router.patch("/{mission_id}/assign", response_model=MissionResponse)
async def assign_cat(mission_id: int, data: MissionAssignCat, db: AsyncSession = Depends(get_db)):
    try:
        return await assign_cat_to_mission(db, mission_id, data.cat_id)
    except ValueError as e:
        if str(e) == "Cat does not exist" or str(e) == "Mission does not exist":
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MissionResponse])
async def get_all_missions(db: AsyncSession = Depends(get_db)):
    return await list_missions(db)

@router.get("/{mission_id}", response_model=MissionResponse)
async def get_single_mission(mission_id: int, db: AsyncSession = Depends(get_db)):
    mission = await get_mission(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission