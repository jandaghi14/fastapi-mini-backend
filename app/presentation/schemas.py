from pydantic import BaseModel, model_validator, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.core import enums


class UserCreate(BaseModel):
    username : str = Field(min_length=3)
    password : str = Field(min_length= 8)
    role : enums.UserRole = enums.UserRole.user
    
class UserShow(BaseModel):
    id : int
    username : str
    role : enums.UserRole = enums.UserRole.user
    model_config = ConfigDict(from_attributes=True)


class TodoCreate(BaseModel):
    title : str = Field(min_length= 3)
    description : str | None = None
    priority : enums.TodoPriority = enums.TodoPriority.low
    due_date : datetime | None = None
    
class TodoShow(BaseModel):
    id : int
    user_id : int
    
    title : str
    description : str | None = None
    
    created_at : datetime
    
    status : enums.TodoStatus
    priority : enums.TodoPriority
    
    is_deleted : bool
    
    updated_at : datetime | None
    due_date : datetime | None
    
    model_config = ConfigDict(from_attributes=True)
        
        
        
class OwnerShow(BaseModel):
    username: str
    role : enums.UserRole
    model_config = ConfigDict(from_attributes=True)

        

class TodoShowWithOwner(BaseModel):
    id : int
    user_id : int
    
    title : str
    description : str | None = None
    
    created_at : datetime
    
    status : enums.TodoStatus
    priority : enums.TodoPriority
    
    is_deleted : bool
    
    owner : OwnerShow
        
    model_config = ConfigDict(from_attributes=True)
        
        
class TodoShowUpdate(TodoShow):
    updated_at : datetime | None
        
class TodoUpdate(BaseModel):
    title : str | None = None
    description : str | None = None
    
    status : enums.TodoStatus | None = None
    priority : enums.TodoPriority | None = None
    
    due_date : datetime | None = None
    
    @model_validator(mode='after')
    def check_completed_todo(self):
        if self.status == enums.TodoStatus.completed and self.priority is not None:
            raise ValueError('The priority of a completed todo cannot be changed!')
        return self
    
class TodoUpdateAdmin(TodoUpdate):
    is_deleted : bool | None = None

    user_id : int | None = None