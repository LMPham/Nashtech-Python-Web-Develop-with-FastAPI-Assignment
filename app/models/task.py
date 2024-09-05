from typing import Optional
from pydantic import BaseModel, Field
from entities.task import TaskStatus
from datetime import datetime
from uuid import UUID

class SearchTaskModel():
    def __init__(self, summary, description, status, priority, page, size) -> None:
        self.summary = summary
        self.description = description
        self.status = status
        self.priority = priority
        self.page = page
        self.size = size

class CreateTaskModel(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.CREATED)
    priority: int = Field(ge=0, le=5, default=0)
    user_id: UUID = Field()
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "FastAPI Development",
                "description": "Implement FastAPI endpoints for the new project.",
                "status": "COMPLETED",
                "priority": "5",
                "user_id": "70123094-777c-4d5b-b47d-9ad4f650e2ca"
            }
        }

class UpdateTaskModel(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(None, ge=0, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "FastAPI Development",
                "description": "Implement FastAPI endpoints for the new project.",
                "status": "COMPLETED",
                "priority": "5"
            }
        }

class TaskViewModel(BaseModel):
    id: UUID 
    summary: str | None = None
    description: str | None = None
    status: TaskStatus
    priority: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True