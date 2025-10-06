from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.targets_schema import TargetUpdate, TargetResponse
from services.target_service import update_target
from db.db import get_db

router = APIRouter(prefix="/targets", tags=["Targets"])

@router.patch("/{target_id}", response_model=TargetResponse)
async def patch_target(
    target_id: int,
    update_data: TargetUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await update_target(db, target_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")