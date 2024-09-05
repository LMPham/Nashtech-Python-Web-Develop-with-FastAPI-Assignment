from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class SearchUserModel():
    def __init__(
        self, 
        email, 
        username, 
        first_name, 
        last_name,
        is_active,
        is_admin,
        page, 
        size
    ) -> None:
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_admin = is_admin
        self.page = page
        self.size = size

class CreateUserModel(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    company_id: UUID = Field()
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Minh",
                "last_name": "Pham Le",
                "is_active": "True",
                "is_admin": "False",
                "company_id": "33fde304-82cf-42bb-8b54-9bf67d4ce056"
            }
        }
        
class UpdateUserModel(BaseModel):
    password: str = Field(None, min_length=6)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "password": "p@ssw0rd123",
                "is_active": "True",
                "is_admin": "False",
            }
        }


class UserViewModel(BaseModel):
    id: UUID 
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    company_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True