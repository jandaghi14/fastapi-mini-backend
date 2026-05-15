from app.infrastructure.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from app.core.enums import TodoStatus,TodoPriority, UserRole
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True)
    
    username = Column(String, nullable= False, index= True ,unique= True)
    password_hash = Column(String, nullable= False)
    
    role = Column(Enum(UserRole, name = 'user_role'), default = UserRole.user)
    
    todos = relationship("Todo", back_populates='owner')
    
    
class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key= True)
    
    title = Column(String,nullable=False)
    description = Column(String,nullable=True)
    
    created_at = Column(DateTime,nullable=False ,server_default=func.now())
    updated_at = Column(DateTime,nullable=True , server_default=func.now(), onupdate=func.now())
    
    status = Column(Enum(TodoStatus, name = 'todo_status'),nullable=False,default=TodoStatus.pending)
    
    is_deleted = Column(Boolean, default=False, index = True)
    
    priority = Column(Enum(TodoPriority,name = 'todo_priority'), default= TodoPriority.low)
    
    user_id = Column(Integer,ForeignKey('users.id'),index=True)
    
    due_date = Column(DateTime,nullable=True)
    
    owner = relationship("User", back_populates='todos')



