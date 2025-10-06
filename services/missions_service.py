from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from models.models import Mission, SpyCat, Target
from schemas.missions_schema import MissionCreate
from schemas.targets_schema import TargetCreate, TargetUpdate
from typing import List

async def create_mission_with_targets(session: AsyncSession, mission_data: MissionCreate) -> Mission:
    mission = Mission(is_completed=mission_data.is_completed)
    session.add(mission)
    await session.flush()
    targets = [Target(mission_id=mission.id, **target.dict()) for target in mission_data.targets]
    session.add_all(targets)
    await session.commit()
    result = await session.execute(
        select(Mission).options(selectinload(Mission.targets)).where(Mission.id == mission.id)
    )
    mission = result.scalar_one()
    return mission

async def delete_mission(session: AsyncSession, mission_id: int) -> None:
    mission = await session.get(Mission, mission_id)
    if mission.cat_id is not None:
        raise ValueError("Cannot delete mission assigned to a cat")
    await session.delete(mission)
    await session.commit()

async def assign_cat_to_mission(session: AsyncSession, mission_id: int, cat_id: int) -> Mission:
    cat = await session.get(SpyCat, cat_id)
    if not cat:
        raise ValueError("Cat does not exist")
    mission = await session.get(Mission, mission_id)
    if not mission:
        raise ValueError("Mission does not exist")
    mission.cat_id = cat_id
    await session.commit()
    result = await session.execute(
        select(Mission).options(selectinload(Mission.targets)).where(Mission.id == mission_id)
    )
    return result.scalar_one()

async def list_missions(session: AsyncSession):
    result = await session.execute(
        select(Mission).options(selectinload(Mission.targets))
    )
    return result.scalars().all()

async def get_mission(session: AsyncSession, mission_id: int):
    result = await session.execute(
        select(Mission).options(selectinload(Mission.targets)).where(Mission.id == mission_id)
    )
    return result.scalar_one_or_none()