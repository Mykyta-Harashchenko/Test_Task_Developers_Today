from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.models import Target, Mission
from schemas.targets_schema import TargetUpdate

async def update_target(session: AsyncSession, target_id: int, update_data: TargetUpdate) -> Target:
    target = await session.get(Target, target_id)
    if not target:
        raise ValueError("Target does not exist")
    mission = await session.get(Mission, target.mission_id)
    if not mission:
        raise ValueError("Mission does not exist")
    if update_data.is_completed is not None and mission.cat_id is None:
        raise ValueError("Cannot update target status: mission is not assigned to a cat")
    if target.is_completed or mission.is_completed:
        if update_data.notes is not None:
            raise ValueError("Cannot update notes if target or mission is completed")
    if update_data.notes is not None:
        target.notes = update_data.notes
    if update_data.is_completed is not None:
        target.is_completed = update_data.is_completed
    await session.commit()
    result = await session.execute(
        select(Target).where(Target.mission_id == mission.id)
    )
    all_targets = result.scalars().all()
    if all_targets and all(t.is_completed for t in all_targets):
        mission.is_completed = True
        await session.commit()
    else:
        if mission.is_completed:
            mission.is_completed = False
            await session.commit()

    await session.refresh(target)
    return target