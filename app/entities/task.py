import enum

from sqlalchemy import Column, Enum, ForeignKey, SmallInteger, String, Uuid
from sqlalchemy.orm import relationship

from database import Base
from entities.base_entity import BaseEntity

class TaskStatus(enum.Enum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Task(BaseEntity, Base):
    __tablename__ = "tasks"
    
    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED)
    priority = Column(SmallInteger, default=0)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User")