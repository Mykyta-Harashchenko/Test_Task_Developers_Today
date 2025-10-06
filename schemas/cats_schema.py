from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class CatCreate(BaseModel):
    name: str
    years_experience: int
    breed: str
    salary: float

    @field_validator("years_experience")
    @classmethod
    def years_experience_non_negative(cls, v):
        if v < 0:
            raise ValueError("Years of experience must be non-negative")
        return v

    @field_validator("salary")
    @classmethod
    def salary_non_negative(cls, v):
        if v < 0:
            raise ValueError("Salary must be non-negative")
        return v

class CatUpdate(BaseModel):
    salary: float

    @field_validator("salary")
    @classmethod
    def salary_non_negative(cls, v):
        if v < 0:
            raise ValueError("Salary must be non-negative")
        return v

class CatResponse(BaseModel):
    id: int
    name: str
    years_experience: int
    breed: str
    salary: float

    class Config:
        from_attributes = True