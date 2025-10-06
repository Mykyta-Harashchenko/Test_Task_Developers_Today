from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.cats_schema import CatCreate, CatUpdate, CatResponse
from services.cat_service import create_cat, delete_cat, update_cat_salary, list_cats, get_cat
from db.db import get_db

router = APIRouter(prefix="/cats", tags=["Spy Cats"])

@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_spy_cat(cat: CatCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_cat(db, cat)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_spy_cat(cat_id: int, db: AsyncSession = Depends(get_db)):
    await delete_cat(db, cat_id)
    return

@router.patch("/{cat_id}", response_model=CatResponse)
async def update_spy_cat_salary(cat_id: int, update: CatUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await update_cat_salary(db, cat_id, update)
    except Exception:
        raise HTTPException(status_code=404, detail="Cat not found")

@router.get("/", response_model=list[CatResponse])
async def get_all_spy_cats(db: AsyncSession = Depends(get_db)):
    return await list_cats(db)

@router.get("/{cat_id}", response_model=CatResponse)
async def get_single_spy_cat(cat_id: int, db: AsyncSession = Depends(get_db)):
    cat = await get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat