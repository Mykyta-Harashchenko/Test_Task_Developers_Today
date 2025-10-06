from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.models import SpyCat
from schemas.cats_schema import CatCreate, CatUpdate
import httpx

CAT_API_URL = "https://api.thecatapi.com/v1/breeds"

async def validate_breed(breed: str) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.get(CAT_API_URL)
        resp.raise_for_status()
        breeds = resp.json()
        return any(b["name"].lower() == breed.lower() or b["id"].lower() == breed.lower() for b in breeds)

async def create_cat(session: AsyncSession, cat_data: CatCreate) -> SpyCat:
    if not await validate_breed(cat_data.breed):
        raise ValueError("Invalid breed")
    cat = SpyCat(**cat_data.dict())
    session.add(cat)
    await session.commit()
    await session.refresh(cat)
    return cat

async def delete_cat(session: AsyncSession, cat_id: int) -> None:
    await session.execute(delete(SpyCat).where(SpyCat.id == cat_id))
    await session.commit()

async def update_cat_salary(session: AsyncSession, cat_id: int, update_data: CatUpdate) -> SpyCat:
    await session.execute(update(SpyCat).where(SpyCat.id == cat_id).values(salary=update_data.salary))
    await session.commit()
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    return result.scalar_one()

async def list_cats(session: AsyncSession):
    result = await session.execute(select(SpyCat))
    return result.scalars().all()

async def get_cat(session: AsyncSession, cat_id: int):
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    return result.scalar_one_or_none()