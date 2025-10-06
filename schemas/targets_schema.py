from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    is_completed: bool = False

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None

class TargetResponse(BaseModel):
    id: int
    name: str
    country: str
    notes: Optional[str]
    is_completed: bool
    mission_id: int
    updated_at: datetime

    class Config:
        from_attributes = True