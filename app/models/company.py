from typing import Optional
from pydantic import BaseModel, Field
from entities.company import CompanyMode
from datetime import datetime
from uuid import UUID

class SearchCompanyModel():
    def __init__(self, name, description, mode, rating, page, size) -> None:
        self.name = name
        self.description = description
        self.mode = mode
        self.rating = rating
        self.page = page
        self.size = size

class CreateCompanyModel(BaseModel):
    name: str = Field()
    description: str = Field()
    mode: CompanyMode = Field(default=CompanyMode.PENDING)
    rating: int = Field(ge=0, le=5, default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nashtech",
                "description": "Create the best solutions, powered by our excellence in people and technology",
                "mode": "ESTABLISHED",
                "rating": "5"
            }
        }

class UpdateCompanyModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[CompanyMode] = None
    rating: Optional[int] = Field(None, ge=0, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nashtech",
                "description": "Create the best solutions, powered by our excellence in people and technology",
                "mode": "ESTABLISHED",
                "rating": "5"
            }
        }

class CompanyViewModel(BaseModel):
    id: UUID 
    name: str | None = None
    description: str | None = None
    mode: CompanyMode
    rating: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True