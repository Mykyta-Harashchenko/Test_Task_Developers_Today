from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from schemas.targets_schema import TargetCreate, TargetResponse

class MissionCreate(BaseModel):
    targets: List[TargetCreate]
    is_completed: bool = False

    @field_validator("targets")
    @classmethod
    def validate_targets(cls, v):
        if not (1 <= len(v) <= 3):
            raise ValueError("You must provide between 1 and 3 targets.")
        names = [target.name for target in v]
        if len(names) != len(set(names)):
            raise ValueError("Each target in a mission must have a unique name.")
        return v

class MissionAssignCat(BaseModel):
    cat_id: int

class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    targets: List[TargetResponse]

    class Config:
        from_attributes = True